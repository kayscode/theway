from organisations.repositories import OrganisationRepository


def generate_organisation_select_form_choices():
    organisations_data = OrganisationRepository.select_id_and_organisations_name()

    organisations_choices = []

    for organisation in organisations_data:
        organisations_choices.append((organisation.get("id"), organisation.get("name")))

    return organisations_choices
