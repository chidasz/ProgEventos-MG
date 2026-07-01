from django import forms
from .models import Competicao
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CompeticaoForm(forms.ModelForm):

    class Meta:
        model = Competicao

        fields = [
            'nome',
            'descricao',
            'data',
            'local',
            'organizador',
            'pessoa',
            'universidade',
            'administrador'
        ]
class CadastroForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = User

        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )