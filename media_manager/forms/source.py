from django import forms
from media_manager.utils import generate_organisation_select_form_choices


class ManagerCreateSourceMediaForm(forms.Form):
    url = forms.URLField(
        label="lien url",
        widget=forms.URLInput(
            attrs={
                'placeholder': 'adresse url',
                'class': 'p-2 rounded-md bg-gray-50 focus:outline-none focus:outline-gray-300'
            }
        )
    )

    source_type = forms.ChoiceField(
        label="type de source",
        widget=forms.Select(
            attrs={
                'placeholder': 'type de source',
                'class': 'p-2 rounded-md bg-gray-50 focus:outline-none focus:outline-gray-300'
            }
        ),
        choices=[
            ("web-scrapping", "web-scrapping"),
            ("api", "api")
        ]
    )


class AdminCreateSourceMediaForm(ManagerCreateSourceMediaForm):
    organisation = forms.ChoiceField(
        label="organisation",
        widget=forms.Select(
            attrs={
                'placeholder': 'branches',
                'class': 'p-2 rounded-md bg-gray-50 focus:outline-none focus:outline-gray-300'
            }
        ),
        choices=generate_organisation_select_form_choices()
    )

    approval_status = forms.ChoiceField(
        label="status",
        choices=[("pending", "en attente"),
                 ("rejected", "rejecter"),
                 ("accepted", "accepter"), ],
        widget=forms.Select(
            attrs={
                'class': 'p-2 rounded-md bg-gray-50 focus:outline-none focus:outline-gray-300'
            }
        )
    )


class DeleteSourceMediaForm(forms.Form):
    id = forms.IntegerField(label="source id", widget=forms.HiddenInput)


class ManagerUpdateSourceMediaForm(ManagerCreateSourceMediaForm):
    id = forms.IntegerField(label="source id", widget=forms.HiddenInput)


class AdminUpdateSourceMediaForm(AdminCreateSourceMediaForm):
    id = forms.IntegerField(label="source id", widget=forms.HiddenInput)
