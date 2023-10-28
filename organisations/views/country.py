from django.shortcuts import render, redirect, reverse

from organisations.repositories.country import CountryRepository
from organisations.models import Country

from organisations.forms import CreateCountryForm, UpdateCountryForm, DeleteCountryForm


def country_list(request):
    if request.user is not None and request.user.is_authenticated:

        context = {
            "countries": CountryRepository.find_all()
        }
        return render(request, "organisations/branches/list_country.html", context)
    else:
        return redirect(reverse("auth_login"))


def show_Country(request, country_id):
    if request.user is not None and request.user.is_authenticated:
        try:

            context = {
                "country": CountryRepository.find_one(country_id)
            }

            return render(request, "organisations/branches/detail_country.html", context)

        except Country.DoesNotExist:
            return redirect(reverse("error_404"))
    else:

        return redirect(reverse("auth_login"))


def create_country(request):
    if request.user is not None and request.user.is_authenticated and request.user.is_super_admin:
        if request.method == "GET":
            country_form = CreateCountryForm()
            context = {
                "form": country_form
            }
            return render(request, "organisations/branches/create_country.html", context)
        elif request.method == "POST":
            country_form = CreateCountryForm(request.POST)

            if country_form.is_valid():
                country = CountryRepository.create(
                    continent=country_form.cleaned_data.get("continent"),
                    name=country_form.cleaned_data.get("name")
                )

                return redirect(reverse("show_country", kwargs={"country_id": country.id}))

            context = {
                "form": country_form
            }
            return render(request, "organisations/branches/create_country.html", context)

    else:
        return redirect(reverse("auth_login"))


def edit_country(request, country_id):
    if request.user is not None and request.user.is_authenticated and request.user.is_super_admin:
        if request.method == "GET":
            try:
                country = CountryRepository.find_one(country_id)
                country_form = CreateCountryForm(country.to_json)
                context = {
                    "form": country_form
                }
                return render(request, "organisations/branches/edit_country.html", context)
            except Country.DoesNotExist:
                return redirect(reverse("error_404"))
        elif request.method == "POST":
            country_form = UpdateCountryForm(request.POST)

            if country_form.is_valid():

                country = CountryRepository.update(
                    country_id=country_form.cleaned_data.get("id"),
                    country_data=country_form.cleaned_data
                )

                return redirect(reverse("show_country", kwargs={"country_id": country.id}))

            context = {
                "form": country_form
            }
            return render(request, "organisations/branches/edit_country.html", context)

    else:
        return redirect(reverse("auth_login"))


def delete_country(request, country_id):
    if request.user is not None and request.user.is_authenticated:
        if request.method == "POST":
            country_form = DeleteCountryForm(request.POST)

            if country_form.is_valid():
                CountryRepository.delete(country_form.cleaned_data.get("id"))
                return redirect(reverse("country_list"))

            return redirect(reverse("show_country",kwargs={"country_id":country_id}))
    else:
        return redirect(reverse("auth_login"))
