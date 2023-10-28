from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder' : "entrez votre username",
            'class' : 'p-2 rounded-md bg-gray-50 focus:outline-none focus:outline-gray-300'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder' : 'entrez votre mot de passe',
            'class' : 'p-2 rounded-md bg-gray-50 focus:outline-none focus:outline-gray-300'
        }
    ))


class LogoutForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput)