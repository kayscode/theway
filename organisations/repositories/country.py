from organisations.models import Country


class CountryRepository:

    @classmethod
    def create(cls, continent: str, name: str):
        return Country.objects.create(
            continent=continent,
            name=name
        )

    @classmethod
    def find_one(cls, country_id: int):
        return Country.objects.get(id=country_id)

    @classmethod
    def find_by_name(cls, name: str):
        return Country.objects.get(name=name)

    @classmethod
    def find_all(cls):
        return Country.objects.all()

    @classmethod
    def update(cls, country_id, country_data):
        country = cls.find_one(country_id)
        country.name = country_data["name"]
        country.continent = country_data["continent"]

        return country.save()

    @classmethod
    def delete(cls, country_id):
        country = cls.find_one(country_id)
        country.delete()

    @classmethod
    def select_id_and_country_name(cls):
        return Country.objects.all(["id","name"])