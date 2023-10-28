import datetime

import django.utils.timezone
from django.db import models
from django_softdelete.models import SoftDeleteModel
from organisations.models import Organisations, User


# Create your models here.
class SourceMediaFile(SoftDeleteModel):
    url = models.URLField(blank=False, null=False)
    source_type = models.CharField(
        choices=[
            ("api", "api"),
            ("web-scrapping", "web-scrapping")
        ],
        null=False,
        blank=False
    )
    approval_status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "en attente"),
            ("rejected", "rejecter"),
            ("accepted", "accepter"),
        ],
        default="pending"
    )
    organisation = models.ForeignKey(Organisations, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now=True)

    @property
    def to_json(self):
        return {
            "organisation": self.organisation.id,
            "source_type": self.source_type,
            "url": self.url,
            "status": self.approval_status,
            "created" : self.created
        }

    class Meta:
        db_table = "sources"


class MediaFile(SoftDeleteModel):
    title = models.CharField(max_length=200, null=False, blank=False)
    file_cover = models.ImageField(null=False, blank=False, upload_to="media_covers")
    file = models.FileField(null=False, blank=False, upload_to="media_files")
    organisation = models.ForeignKey(Organisations, on_delete=models.CASCADE, null=True, blank=True)
    uploaded_date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "en attente"),
            ("rejected", "rejecter"),
            ("accepted", "accepter"),
        ],
        default="pending"
    )
    media_type = models.CharField(
        choices=[
            ("video", "video"),
            ("audio", "audio")
        ],
        null=False,
        blank=False
    )

    @property
    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "file_cover": self.file_cover,
            "file": self.file.url,
            "organisation": self.organisation.id,
            "uploaded_date": self.uploaded_date,
            "status": self.status,
            "media_type": self.media_type
        }

    def __repr__(self):
        return f"{self.title} ({self.media_type})"

    class Meta:
        db_table = "medias"


class AbstractNotifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=False, blank=False)
    validation_date = models.DateField(null=True, blank=True)
    request_type = models.CharField(
        max_length=20,
        default="creation-request",
        choices=[
            ("creation-request", "creation-request"),
            ("deletion-request", "delete-request"),
        ]
    )
    sent_date = models.DateField(default=django.utils.timezone.now())
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "en attente"),
            ("rejected", "rejecter"),
            ("accepted", "accepter"),
        ],
        default="pending"
    )

    @property
    def to_json(self):
        return {
            "id": self.id,
            "user": self.user.id,
            "description": self.description,
            "validation_date": self.validation_date,
            "is_validated": self.is_validated,
            "sent_date": self.sent_date,
            "status": self.status
        }

    class Meta:
        abstract = True


class Notifications(SoftDeleteModel, AbstractNotifications):
    media = models.ForeignKey(MediaFile, on_delete=models.SET_NULL, null=True)

    @property
    def to_json(self):
        notification = super().to_json
        notification["media"] = self.media.id
        return notification

    class Meta:
        db_table = "notifications"
        abstract = False


class NotificationsSourceMedia(SoftDeleteModel, AbstractNotifications):
    source = models.ForeignKey(SourceMediaFile, on_delete=models.SET_NULL, null=True)

    @property
    def to_json(self):
        notification = super().to_json
        notification["source"] = self.source_id
        return notification

    class Meta:
        db_table = "source_notifications"
        abstract = False
