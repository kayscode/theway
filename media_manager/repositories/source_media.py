from media_manager.models import SourceMediaFile
from organisations.models import Organisations


class SourceMediaRepository:

    @classmethod
    def create(cls, source_form_data):

        source = SourceMediaFile(
            url=source_form_data.get("url"),
            source_type=source_form_data.get("source_type"),
            organisation=Organisations.objects.get(id=source_form_data.get("organisation"))
        )

        if source_form_data.get("approval_status") is not None:
            source.approval_status = source_form_data.get("approval_status")

        source.save()
        return source

    @classmethod
    def find_one(cls, source_id):
        source_media = SourceMediaFile.objects.get(id=source_id)

        if source_media:
            return source_media
        else:
            raise SourceMediaFile.DoesNotExist

    @classmethod
    def find_all(cls):
        return SourceMediaFile.objects.all().order_by("created")

    @classmethod
    def filter_by(cls, status="pending"):
        return SourceMediaFile.objects.filter(approval_status=status).order_by("created")

    @classmethod
    def filter_by_source_type(cls, source_type: str):
        return SourceMediaFile.objects.all().filter(source_type__exact=source_type)

    @classmethod
    def delete(cls, source_id):
        source_media = cls.find_one(source_id)
        return source_media.delete()

    @classmethod
    def update(cls, source_id, source_data):

        source = cls.find_one(source_id)

        source.url = source_data.get("url")
        source.organisation = Organisations.objects.get(id=source_data.get("organisation"))
        source.source_type = source_data.get("source_type")
        source.approval_status = source_data.get("approval_status")

        return source.save()

    @classmethod
    def filter_by_organisation_id(cls, organisation_id):
        return cls.find_all().filter(organisation=organisation_id)

    @classmethod
    def approve_uploaded_source(cls, source_id):
        source_media = cls.find_one(source_id)
        source_media.approval_status = "accepted"
        return source_media.save()

    @classmethod
    def reject_uploaded_source(cls, source_id):
        source_media = cls.find_one(source_id)
        source_media.approval_status = "rejected"
        return source_media.save()