from django import forms


class CreateCountryForm(forms.Form):
    continent = forms.ChoiceField(
        label="continent",
        widget=forms.Select(
            attrs={
                "class": "p-2 rounded-md bg-gray-50 focus:outline-none focus:outline-gray-300",
                "rows": 2
            }
        ),
        choices=[
            ("Af", "Afrique"),
            ("Eu", "Europe"),
            ("Asie", "Asie"),
            ("Amerique", "Amerique"),
            ("Oceanie", "Oceanie"),
        ],
    )
    name = forms.CharField(
        label="nom du pays",
        widget=forms.TextInput(
            attrs={
                "class": "p-2 rounded-md bg-gray-50 focus:outline-none focus:outline-gray-300",
                "rows": 2
            }
        )
    )


class DeleteCountryForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput)


class UpdateCountryForm(CreateCountryForm, DeleteCountryForm):
    pass
