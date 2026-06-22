from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login
from .forms import CompeticaoForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from .models import (
    Competicao,
    Universidade,
    Resultado
)

# =========================
# PÁGINA INICIAL
# =========================

class IndexView( View):

    def get(self, request):

        proximas_competicoes = Competicao.objects.order_by('data')[:4]

        context = {

            'usuario': request.user,

            'total_competicoes':
                Competicao.objects.count(),

            'total_universidades':
                Universidade.objects.count(),

            'total_resultados':
                Resultado.objects.count(),

            'proximas_competicoes':
                proximas_competicoes,

            'avatar_usuario':
                request.session.get('avatar_usuario')

        }

        return render(
            request,
            'index.html',
            context
        )

# =========================
# LOGIN
# =========================

class LoginView(View):

    def post(self, request):

        username = request.POST.get("nome")
        password = request.POST.get("senha")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('/')

        return render(
            request,
            "login.html",
            {
                "erro": "Usuário ou senha inválidos."
            }
        )


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
            {'administracoes': administracoes}
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
            {'universidades': universidades}
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
            {'competicoes': competicoes}
        )


# CORRIGIDO: delete via POST com CSRF
class DeleteCompeticaoView(LoginRequiredMixin, View):
    def post(self, request, id):
        competicao = get_object_or_404(Competicao, id=id)
        competicao.delete()
        return redirect('competicoes')


class EditarCompeticaoView(LoginRequiredMixin, View):

    def get(self, request, id):
        competicao = get_object_or_404(Competicao, id=id)
        form = CompeticaoForm(instance=competicao)

        return render(
            request,
            'editar_competicao.html',
            {'form': form}
        )

    def post(self, request, id):
        competicao = get_object_or_404(Competicao, id=id)
        form = CompeticaoForm(request.POST, instance=competicao)

        if form.is_valid():
            form.save()
            return redirect('competicoes')

        return render(
            request,
            'editar_competicao.html',
            {'form': form}
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
            {'resultados': resultados}
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
            {'calendarios': calendarios}
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
            {'notificacoes': notificacoes}
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
            {'favoritos': favoritos}
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
            {'historicos': historicos}
        )


# =========================
# PESQUISA
# =========================

class PesquisaView(View):

    def get(self, request):
        pesquisa    = request.GET.get('pesquisa', '')
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
                'pesquisa':    pesquisa
            }
        )


# =========================
# LOGOUT
# =========================

class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('index')