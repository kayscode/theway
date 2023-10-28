from django import forms
from organisations.utils import generate_organisation_select_form_choices


class CreateUserForm(forms.Form):
    avatar = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                "class": "p-2 rounded-md bg-gray-50 focus:outline-none focus:outline-gray-300"
            }
        ),
        required=False
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "p-2 rounded-md bg-gray-50 focus:outline-none focus:outline-gray-300"
            }
        )
    )


class AdminCreateUserForm(CreateUserForm):
    username = forms.CharField( label="utilisateur",
        widget=forms.TextInput(
            attrs={
                "class": "p-2 rounded-md bg-gray-50 focus:outline-none focus:outline-gray-300",
            }
        )
    )

    email = forms.EmailField( label="email",
        widget=forms.EmailInput(
            attrs={
                "class": "p-2 rounded-md bg-gray-50 focus:outline-none focus:outline-gray-300"
            }
        )
    )

    organisation= forms.ChoiceField(label="branche",
        choices=generate_organisation_select_form_choices(),
        widget=forms.Select(
            attrs={
                "class": "p-2 rounded-md bg-gray-50 focus:outline-none focus:outline-gray-300"
            }
        )
    )

    account_type = forms.ChoiceField(label="role",
        choices=[
            ("admin", "admin"),
            ("super admin", "gestionnaire")
        ],
        widget=forms.Select(
            attrs={
                "class": "p-2 rounded-md bg-gray-50 focus:outline-none focus:outline-gray-300"
            }
        )
    )

    is_active = forms.BooleanField( label="activer ?",
        widget=forms.CheckboxInput(
            attrs={
                "class": "p-2 rounded-md bg-gray-50 focus:outline-none focus:outline-gray-300 text-left"
            }
        )
    )


class DeleteUserForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput)


class UpdateUserForm(CreateUserForm, DeleteUserForm):
    pass


class AdminUpdateUserForm(DeleteUserForm, AdminCreateUserForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "p-2 rounded-md bg-gray-50 focus:outline-none focus:outline-gray-300"
            }
        ),
        required=False
    )

    is_active = forms.BooleanField(
        label="activer ?",
        widget=forms.CheckboxInput(
            attrs={
                "class": "p-2 rounded-md bg-gray-50 focus:outline-none focus:outline-gray-300 text-left"
            }
        ),
        required=False
    )
