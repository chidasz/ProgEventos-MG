from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import *
from .forms import CompeticaoForm


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class PessoasView(View):
    def get(self, request):
        pessoas = Pessoa.objects.all()
        return render(request, 'pessoa.html', {'pessoas': pessoas})


class AdministracoesView(View):
    def get(self, request):
        administracoes = Administracao.objects.all()
        return render(request, 'administracao.html', {'administracoes': administracoes})


class UniversidadesView(View):
    def get(self, request):
        universidades = Universidade.objects.all()
        return render(request, 'universidade.html', {'universidades': universidades})


class CompeticoesView(View):
    def get(self, request):
        competicoes = Competicao.objects.all()
        return render(request, 'competicao.html', {'competicoes': competicoes})


class ResultadosView(View):
    def get(self, request):
        resultados = Resultado.objects.all()
        return render(request, 'resultado.html', {'resultados': resultados})


class CalendariosView(View):
    def get(self, request):
        calendarios = Calendario.objects.all()
        return render(request, 'calendario.html', {'calendarios': calendarios})


class NotificacoesView(View):
    def get(self, request):
        notificacoes = Notificacao.objects.all()
        return render(request, 'notificacao.html', {'notificacoes': notificacoes})


class DeleteCompeticaoView(View):
    def get(self, request, id):
        competicao = Competicao.objects.get(id=id)
        competicao.delete()
        return redirect('competicoes')


class EditarCompeticaoView(View):
    def get(self, request, id):
        competicao = get_object_or_404(Competicao, id=id)
        form = CompeticaoForm(instance=competicao)
        return render(request, 'editar_competicao.html', {'form': form})

    def post(self, request, id):
        competicao = get_object_or_404(Competicao, id=id)
        form = CompeticaoForm(request.POST, instance=competicao)

        if form.is_valid():
            form.save()
            return redirect('competicoes')

        return render(request, 'editar_competicao.html', {'form': form})