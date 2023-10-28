from django import forms
from media_manager.utils import generate_organisation_select_form_choices


class ManagerCreateMediaFileForm(forms.Form):
    title = forms.CharField(
        label="titre",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'entrez votre mot de passe',
                'class': 'p-2 rounded-md bg-gray-50 focus:outline-none focus:outline-gray-300'
            }
        )
    )

    file_cover = forms.ImageField(
        label="image",
        widget=forms.FileInput(
            attrs={
                'placeholder': 'entrez votre mot de passe',
                'class': 'p-2 rounded-md bg-gray-50 focus:outline-none focus:outline-gray-300'
            }
        ),
        required=False
    )

    file = forms.FileField(
        label="uploader fichier",
        widget=forms.FileInput(
            attrs={
                'placeholder': 'entrez votre mot de passe',
                'class': 'p-2 rounded-md bg-gray-50 focus:outline-none focus:outline-gray-300'
            }
        ),
    )

    media_type = forms.ChoiceField(
        label="type de fichier",
        widget=forms.Select(
            attrs={
                'placeholder': 'entrez votre mot de passe',
                'class': 'p-2 rounded-md bg-gray-50 focus:outline-none focus:outline-gray-300'
            }
        ),
        choices=[
            ("audio", "audio"),
            ("video", "video")
        ]
    )


class AdminCreateMediaFileForm(ManagerCreateMediaFileForm):
    organisation = forms.ChoiceField(
        label="branche",
        widget=forms.Select(
            attrs={
                'placeholder': 'entrez votre mot de passe',
                'class': 'p-2 rounded-md bg-gray-50 focus:outline-none focus:outline-gray-300'
            }
        ),
        choices=generate_organisation_select_form_choices()
    )

    is_approved = forms.BooleanField(
        label="fichier approuver ?",
        widget=forms.CheckboxInput(
            attrs={
                'class': 'p-2 rounded-md bg-gray-50 focus:outline-none focus:outline-gray-300'
            }
        )
    )


class DeleteMediaFileForm(forms.Form):
    id = forms.IntegerField(label="id", widget=forms.HiddenInput)


class ManagerUpdateMediaFileForm(ManagerCreateMediaFileForm):
    file = forms.FileField(
        label="uploader fichier",
        widget=forms.FileInput(
            attrs={
                'placeholder': 'entrez votre mot de passe',
                'class': 'p-2 rounded-md bg-gray-50 focus:outline-none focus:outline-gray-300'
            }
        ),
        required=False
    )
    id = forms.IntegerField(label="id", widget=forms.HiddenInput)


class AdminUpdateMediaFileForm(AdminCreateMediaFileForm):
    file = forms.FileField(
        label="uploader fichier",
        widget=forms.FileInput(
            attrs={
                'placeholder': 'entrez votre mot de passe',
                'class': 'p-2 rounded-md bg-gray-50 focus:outline-none focus:outline-gray-300'
            }
        ),
        required=False
    )
    is_approved = forms.BooleanField(
        label="fichier approuver ?",
        widget=forms.CheckboxInput(
            attrs={
                'class': 'p-2 rounded-md bg-gray-50 focus:outline-none focus:outline-gray-300'
            }
        ),
        required=False
    )
    id = forms.IntegerField(label="id", widget=forms.HiddenInput)
