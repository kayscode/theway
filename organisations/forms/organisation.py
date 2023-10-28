from django import forms
from organisations.utils import get_country_list


class CreateOrganisationForm(forms.Form):
    name = forms.CharField(
        label="nom de la branche",
        widget=forms.TextInput(
            attrs={
                "class":"p-2 rounded-md bg-gray-50 focus:outline-none focus:outline-gray-300",
            }
    ))

    email = forms.EmailField(
        label="email",
        widget=forms.EmailInput(
            attrs={
                "class": "p-2 rounded-md bg-gray-50 focus:outline-none focus:outline-gray-300"
            }
        ))

    country = forms.ChoiceField(
        label="pays",
        widget=forms.Select(
            attrs={
                "class": "p-2 rounded-md bg-gray-50 focus:outline-none focus:outline-gray-300"
            }
        ),
        choices=get_country_list()
    )

    address = forms.CharField(
        label="address",
        widget=forms.Textarea(
            attrs={
                "class": "p-2 rounded-md bg-gray-50 focus:outline-none focus:outline-gray-300",
                "rows" : 2
            }
        ))

    cover = forms.ImageField(
        label="cover",
        widget=forms.FileInput(
            attrs={
                "class": "p-2 rounded-md bg-gray-50 focus:outline-none focus:outline-gray-300"
            }
        ),required=False)


class DeleteOrganisationForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput)


class UpdateOrganisationForm(CreateOrganisationForm, DeleteOrganisationForm):
    pass
