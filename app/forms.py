from django import forms
from django.contrib.auth.models import User

from .models import (
    Perfil,
    Competicao
)


# =====================================
# LOGIN
# =====================================

class LoginForm(forms.Form):

    username = forms.CharField(
        label="Usuário",
        max_length=150
    )

    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput()
    )


# =====================================
# CADASTRO
# =====================================

class CadastroForm(forms.Form):

    username = forms.CharField(
        label="Usuário",
        max_length=150
    )

    email = forms.EmailField()

    senha = forms.CharField(
        widget=forms.PasswordInput()
    )

    universidade = forms.CharField(
        required=False
    )

    avatar = forms.ChoiceField(
        choices=[
            ("homem", "Homem"),
            ("mulher", "Mulher"),
            ("neutro", "Neutro"),
        ],
        initial="neutro"
    )

    foto = forms.ImageField(
        required=False
    )


# =====================================
# PERFIL
# =====================================

class PerfilForm(forms.ModelForm):

    username = forms.CharField()

    email = forms.EmailField()

    senha = forms.CharField(
        widget=forms.PasswordInput(),
        required=False
    )

    class Meta:

        model = Perfil

        fields = [
            "foto",
            "avatar",
            "universidade"
        ]


# =====================================
# COMPETIÇÃO
# =====================================

class CompeticaoForm(forms.ModelForm):

    class Meta:

        model = Competicao

        exclude = [
            "usuario"
        ]

        widgets = {

            "data": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "descricao": forms.Textarea(
                attrs={
                    "rows": 4
                }
            ),

        }