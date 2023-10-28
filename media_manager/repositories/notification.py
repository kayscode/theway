from django.core.exceptions import ObjectDoesNotExist
import datetime

from media_manager.models import Notifications, NotificationsSourceMedia
# from media_manager.repositories import MediaFileRepository, SourceMediaRepository
from .media_file import MediaFileRepository
from .source_media import SourceMediaRepository

from media_manager.models import User,MediaFile,SourceMediaFile


class NotificationsRepository:

    @classmethod
    def create(cls, notification_data):
        notification = Notifications(
            user=User.objects.get(id=notification_data.get("user")),
            media=MediaFile.objects.get(id=notification_data.get("media")),
            description=notification_data.get("description"),
        )
        if notification_data.get("request_type") is None:
            notification.save()
        elif notification_data.get("request_type") is not None:
            notification.request_type = notification_data.get("request_type")
            notification.save()

        return notification

    @classmethod
    def find_all(cls):
        return Notifications.objects.all().order_by("-sent_date")

    @classmethod
    def find_one(cls, notification_id):
        notification = Notifications.objects.get(id=notification_id)
        if notification is None:
            raise Notifications.DoesNotExist

        return notification

    @classmethod
    def approve_notification(cls, notification_id):
        notification = cls.find_one(notification_id)

        notification.status = "accepted"
        notification.validation_date = datetime.date.today()
        notification.save()

        if notification.request_type == "creation-request":
            MediaFileRepository.approve_uploaded_file(notification.media.id)
        elif notification.request_type == "deletion-request":
            # print(f"deletion of {notification.id} with media {notification.media.id}")
            MediaFileRepository.delete(media_id=notification.media.id)

        return notification

    @classmethod
    def reject_notification(cls, notification_id):

        notification = cls.find_one(notification_id)

        if notification.request_type == "creation-request":
            notification.validation_date = datetime.date.today()
            notification.status = "rejected"
            notification.save()

            # reject uploaded file
            MediaFileRepository.reject_uploaded_file(notification.media.id)
        else:
            notification.validation_date = datetime.date.today()
            notification.status = "rejected"
            notification.save()

        return notification

    @classmethod
    def delete(cls, notification_id):
        notification = cls.find_one(notification_id)
        return notification.delete()


class SourceMediaNotificationsRepository:

    @classmethod
    def create(cls, notification_data):
        return NotificationsSourceMedia.objects.create(
            user=User.objects.get(notification_data.get("user")),
            source=SourceMediaFile.objects.get(notification_data.get("media")),
            description=notification_data.get("description"),
        )

    @classmethod
    def find_all(cls):
        return NotificationsSourceMedia.objects.all()

    # @classmethod
    # def find_all_by_notification_type(cls, notification_type=None):
    #     if notification_type is None:
    #         return cls.find_all()
    #     elif notification_type == "source":
    #         return cls.find_all().filter()

    @classmethod
    def find_one(cls, notification_id):
        notification = NotificationsSourceMedia.objects.get(id=notification_id)
        if notification is None:
            raise NotificationsSourceMedia.DoesNotExist

        return notification

    @classmethod
    def approve_notification(cls, notification_id):

        notification = cls.find_one(notification_id)

        if notification.request_type == "creation-request":
            notification.validation_date = datetime.date.today()
            notification.status = "accepted"
            notification.save()

            SourceMediaRepository.approve_uploaded_source(notification.source.id)
        elif notification.request_type == "deletion-request":
            notification.validation_date = datetime.date.today()
            notification.status = "accepted"
            notification.save()

            SourceMediaRepository.delete(source_id=notification.source.id)

        return notification

    @classmethod
    def reject_notification(cls, notification_id):

        notification = cls.find_one(notification_id)

        if notification.request_type == "creation-request":
            notification.validation_date = datetime.date.today()
            notification.status = "rejected"
            notification.save()

            # reject uploaded file
            SourceMediaRepository.reject_uploaded_source(notification.source.id)
        elif notification.request_type == "deletion-request":
            notification.validation_date = datetime.date.today()
            notification.status = "rejected"
            notification.save()

        return notification

    @classmethod
    def delete(cls, notification_id):
        notification = cls.find_one(notification_id)
        return notification.delete()
