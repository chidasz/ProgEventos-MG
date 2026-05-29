from django import forms
from .models import Competicao


class CompeticaoForm(forms.ModelForm):
    class Meta:
        model = Competicao
        fields = '__all__'