from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from .models import *
from .forms import CompeticaoForm


# =========================
# PÁGINA INICIAL
# =========================

class IndexView(View):

    def get(self, request):

        return render(
            request,
            'index.html',
            {
                'nome_usuario':
                    request.session.get('nome_usuario'),

                'avatar_usuario':
                    request.session.get('avatar_usuario')
            }
        )

# =========================
# LOGIN
# =========================

class LoginView(View):

    def get(self, request):
        return render(request, "login.html")

    def post(self, request):

        administrador = request.POST.get("admin")

        if administrador:

            return redirect("/admin/login/")

        nome = request.POST.get("nome")

        request.session["nome_usuario"] = nome

        return redirect("/")


# =========================
# PERFIL
# =========================

class PerfilView(View):
    def get(self, request):
        perfis = Perfil.objects.all()
        return render(
            request,
            'perfil.html',
            {'perfis': perfis}
        )


# =========================
# ADMINISTRAÇÃO
# =========================

class AdministracoesView(View):
    def get(self, request):
        administracoes = Administracao.objects.all()

        return render(
            request,
            'administracao.html',
            {
                'administracoes': administracoes
            }
        )


# =========================
# UNIVERSIDADES
# =========================

class UniversidadesView(View):
    def get(self, request):
        universidades = Universidade.objects.all()

        return render(
            request,
            'universidade.html',
            {
                'universidades': universidades
            }
        )


# =========================
# COMPETIÇÕES
# =========================

class CompeticoesView(View):
    def get(self, request):
        competicoes = Competicao.objects.all()

        return render(
            request,
            'competicao.html',
            {
                'competicoes': competicoes
            }
        )


class DeleteCompeticaoView(View):
    def get(self, request, id):
        competicao = get_object_or_404(
            Competicao,
            id=id
        )

        competicao.delete()

        return redirect('competicoes')


class EditarCompeticaoView(View):

    def get(self, request, id):

        competicao = get_object_or_404(
            Competicao,
            id=id
        )

        form = CompeticaoForm(
            instance=competicao
        )

        return render(
            request,
            'editar_competicao.html',
            {
                'form': form
            }
        )

    def post(self, request, id):

        competicao = get_object_or_404(
            Competicao,
            id=id
        )

        form = CompeticaoForm(
            request.POST,
            instance=competicao
        )

        if form.is_valid():
            form.save()
            return redirect('competicoes')

        return render(
            request,
            'editar_competicao.html',
            {
                'form': form
            }
        )


# =========================
# RESULTADOS
# =========================

class ResultadosView(View):
    def get(self, request):

        resultados = Resultado.objects.all()

        return render(
            request,
            'resultado.html',
            {
                'resultados': resultados
            }
        )


# =========================
# CALENDÁRIOS
# =========================

class CalendariosView(View):
    def get(self, request):

        calendarios = Calendario.objects.all()

        return render(
            request,
            'calendario.html',
            {
                'calendarios': calendarios
            }
        )


# =========================
# NOTIFICAÇÕES
# =========================

class NotificacoesView(View):
    def get(self, request):

        notificacoes = Notificacao.objects.all()

        return render(
            request,
            'notificacao.html',
            {
                'notificacoes': notificacoes
            }
        )


# =========================
# FAVORITOS
# =========================

class FavoritosView(View):
    def get(self, request):

        favoritos = Favorito.objects.all()

        return render(
            request,
            'favoritos.html',
            {
                'favoritos': favoritos
            }
        )


# =========================
# HISTÓRICO
# =========================

class HistoricosView(View):
    def get(self, request):

        historicos = Historico.objects.all()

        return render(
            request,
            'historicos.html',
            {
                'historicos': historicos
            }
        )


# =========================
# PESQUISA
# =========================

class PesquisaView(View):

    def get(self, request):

        pesquisa = request.GET.get(
            'pesquisa',
            ''
        )

        competicoes = Competicao.objects.all()

        if pesquisa:
            competicoes = Competicao.objects.filter(
                nome__icontains=pesquisa
            )

        return render(
            request,
            'pesquisa.html',
            {
                'competicoes': competicoes,
                'pesquisa': pesquisa
            }
        )
    
# =========================
# LOGOUT
# =========================

class LogoutView(View):

    def get(self, request):

        request.session.flush()

        return redirect('index')