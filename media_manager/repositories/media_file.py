from media_manager.models import MediaFile
from organisations.repositories import OrganisationRepository
from organisations.models import Organisations

class MediaFileRepository:

    @classmethod
    def find_all(cls):
        return MediaFile.objects.all()

    @classmethod
    def find_one(cls, media_id):
        media = MediaFile.objects.get(id=media_id)

        if media is None:
            raise MediaFile.DoesNotExist

        return media

    @classmethod
    def create(cls, media_data):
        return MediaFile.objects.create(
            title=media_data.get("title"),
            file_cover=media_data.get("file_cover"),
            file=media_data.get("file"),
            organisation=OrganisationRepository.find_one(media_data.get("organisation")),
            media_type=media_data.get("media_type")
        )

    @classmethod
    def update(cls, media_id, media_data):
        media = cls.find_one(media_id)

        media.title = media_data.get("title")

        if media_data.get("file_cover") is not None:
            media.file_cover = media_data.get("file_cover")

        if media_data.get("file") is not None:
            media.file = media_data.get("file")

        if media_data.get("organisation") is not None:
            media.organisation = Organisations.objects.get(id=media_data.get("organisation"))

        if media_data.get("is_approved") is not None:
            if media_data.get("is_approved") is True:
                media.status = "accepted"
            elif media.data.get("is_approved") is False:
                media.status = "rejected"

        media.media_type = media_data.get("media_type")

        return media.save()

    @classmethod
    def approve_uploaded_file(cls, media_id):
        media = cls.find_one(media_id)
        media.status = "accepted"
        return media.save()

    @classmethod
    def reject_uploaded_file(cls, media_id):
        media = cls.find_one(media_id)
        media.status = "rejected"
        return media.save()

    @classmethod
    def delete(cls, media_id):
        media = cls.find_one(media_id)
        if media is not None:
            return media.delete()

    @classmethod
    def find_by_organisation_id(cls, organisation_id):
        return cls.find_all().filter(organisation=organisation_id)

    @classmethod
    def find_all_audio(cls, organisation_id=None, count=None):
        if count is None:
            if organisation_id is None:
                return cls.find_all().filter(media_type="audio")
            else:
                return cls.find_all().filter(media_type="audio").filter(organisation_id=organisation_id).exclude(
                    status__in=["pending", "rejected"])
        elif count is not None:
            if organisation_id is None:
                return cls.find_all().filter(media_type="audio")[:count]
            else:
                return cls.find_all().filter(media_type="audio").filter(organisation_id=organisation_id).exclude(
                    status__in=["pending", "rejected"])[:count]

    @classmethod
    def find_all_video(cls, organisation_id=None, count=None):
        if count is None:
            if organisation_id is None:
                return MediaFile.objects.filter(media_type="video")
            else:
                return MediaFile.objects.filter(media_type="video").filter(organisation_id=organisation_id).exclude(
                    status__in=["pending", "rejected"])
        elif count is not None:
            if organisation_id is None:
                return MediaFile.objects.filter(media_type="video")[:count]
            else:
                return MediaFile.objects.filter(media_type="video").filter(organisation_id=organisation_id).exclude(
                    status__in=["pending", "rejected"])[:count]
            # return MediaFile.objects.filter(media_type="video").filter(organisation_id=organisation_id)

    @classmethod
    def find_approved_media(cls,media_type,count=None):
        if count is None:
            return cls.find_all().filter(media_type=media_type).exclude(status__in=["rejected","pending"])
        else:
            return cls.find_all().filter(media_type=media_type).exclude(status__in=["rejected", "pending"])[:count]
    @classmethod
    def filter_by_branche(cls,media_type:str,branche_name:str):
        return cls.find_approved_media(media_type=media_type).filter(organisation__name=branche_name)
