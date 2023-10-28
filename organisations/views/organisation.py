from django.shortcuts import render, redirect, reverse
from organisations.forms import CreateOrganisationForm, DeleteOrganisationForm, UpdateOrganisationForm
from organisations.repositories.organisation import OrganisationRepository

from organisations.models import Organisations


def organisation_list(request):
    if request.user is not None and request.user.is_authenticated:
        context = {
            "branches": OrganisationRepository.find_all()
        }
        return render(request, "organisations/branches/list_branches.html", context)
    else:
        return redirect(reverse("auth_login"))


def show_organisation(request, organisation_id):
    if request.user is not None and request.user.is_authenticated:

        try:
            context = {
                "organisation": OrganisationRepository.find_one(organisation_id)
            }
            return render(request, "organisations/branches/detail_branche.html", context)

        except Organisations.DoesNotExist:
            return redirect(reverse("error_404"))
    else:
        return redirect(reverse("auth_login"))


def create_organisation(request):
    if request.user is not None and request.user.is_authenticated :
        if request.method == "GET":
            organisation_form = CreateOrganisationForm()
            context = {
                "form": organisation_form
            }
            return render(request, "organisations/branches/create_branche.html", context)

        if request.method == "POST":
            organisation_form = CreateOrganisationForm(request.POST)
            if organisation_form.is_valid():
                organisation = organisation_form.cleaned_data
                persisted_organisation = OrganisationRepository.create(organisation)
                return redirect(reverse("show_organisation",kwargs={"organisation_id":persisted_organisation.id}))

            context = {
                "form": organisation_form
            }
            return render(request, "organisations/branches/create_branche.html", context)


def edit_and_update_organisation(request, organisation_id):
    if request.method == "GET":
        try:
            organisation = OrganisationRepository.find_one(organisation_id)

            if organisation is None:
                raise Organisations.DoesNotExist

            organisation_form = UpdateOrganisationForm(organisation.to_json)

            context = {
                "form": organisation_form
            }
            return render(request, "organisations/branches/edit_branche.html", context)

        except Organisations.DoesNotExist:
            context = {
                "error": "organisation doesn't exist"
            }
            return redirect(reverse("error_404"))

    elif request.method == "POST":
        organisation_form = UpdateOrganisationForm(request.POST)

        if organisation_form.is_valid():

            organisation_data = organisation_form.cleaned_data
            organisation = OrganisationRepository.find_one(organisation_id)

            if organisation is not None:
                OrganisationRepository.update(organisation_id, organisation_data)
                return redirect(reverse("show_organisation",kwargs={"organisation_id":organisation_id}))

            return render(request, "")

        context = {
            "organisation_form": organisation_form
        }

        return render(request, "organisations/branches/edit_branche.html", context)


def delete_organisation(request):
    if request.method == "POST":
        form = DeleteOrganisationForm(request.POST)

        if form.is_valid():
            OrganisationRepository.delete(form.cleaned_data.get("id"))
            return redirect(reverse("organisation_list"))
        context = {
            "form": form
        }

        return render(request, "", context)
