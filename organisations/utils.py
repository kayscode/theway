from organisations.repositories import CountryRepository
from organisations.repositories import OrganisationRepository


def get_country_list():
    countries = CountryRepository.find_all()
    country_choices = []

    for country in countries:
        country_choices.append((country.id,country.name))

    return country_choices


def generate_organisation_select_form_choices():
    organisations_data = OrganisationRepository.select_id_and_organisations_name()
    organisations_choices = []

    for organisation in organisations_data:
        organisations_choices.append((organisation.get("id"), organisation.get("name")))

    return organisations_choices
