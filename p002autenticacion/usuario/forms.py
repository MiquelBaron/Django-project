from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario', required=True)
    password = forms.CharField(label='Contraseña', required=True, widget=forms.PasswordInput)