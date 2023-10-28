from organisations.models import Organisations
from ..models import Country


class OrganisationRepository:

    @classmethod
    def create(cls, organisation_data):
        return Organisations.objects.create(
            name=organisation_data.get("name"),
            country=Country.objects.get(id=organisation_data.get("country")),
            address=organisation_data.get("address"),
            cover=organisation_data.get("cover"),
            email=organisation_data.get("email")
        )

    @classmethod
    def find_one(cls, organisation_id):
        return Organisations.objects.get(id=organisation_id)

    @classmethod
    def find_by_name(cls):
        pass

    @classmethod
    def find_all(cls):
        return Organisations.objects.all()

    @classmethod
    def delete(cls, organisation_id):
        organisation = cls.find_one(organisation_id)
        return organisation.delete()

    @classmethod
    def update(cls, organisation_id, organisation_data):
        organisation = cls.find_one(organisation_id)
        organisation.name = organisation_data.get("name")
        organisation.country = organisation_data.get("country")
        organisation.cover = organisation_data.get("cover")
        organisation.email = organisation_data.get("email")

        return organisation.save()

    @classmethod
    def select_id_and_organisations_name(cls):
        return Organisations.objects.values("id", "name")
