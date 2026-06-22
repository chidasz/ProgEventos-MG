from django import forms
from .models import Competicao

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