from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from .models import *
from .forms import *


# =====================================
# PÁGINA INICIAL
# =====================================

class IndexView(LoginRequiredMixin, View):

    def get(self, request):

        return render(
            request,
            "index.html"
        )


# =====================================
# LOGIN
# =====================================

class LoginView(View):

    def get(self, request):

        form = LoginForm()

        return render(
            request,
            "login.html",
            {
                "form": form
            }
        )

    def post(self, request):

        username = request.POST.get("username")

        senha = request.POST.get("senha")

        usuario = authenticate(
            request,
            username=username,
            password=senha
        )

        if usuario:

            login(request, usuario)

            return redirect("index")

        return render(
            request,
            "login.html",
            {
                "erro": "Usuário ou senha inválidos."
            }
        )


# =====================================
# LOGOUT
# =====================================

class LogoutView(View):

    def get(self, request):

        logout(request)

        return redirect("login")


# =====================================
# CADASTRO
# =====================================

class CadastroView(View):

    def get(self, request):

        form = CadastroForm()

        return render(
            request,
            "cadastro.html",
            {
                "form": form
            }
        )

    def post(self, request):

        form = CadastroForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            usuario = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["senha"]
            )

            Perfil.objects.create(
                usuario=usuario,
                avatar=form.cleaned_data.get("avatar"),
                foto=form.cleaned_data.get("foto"),
                universidade=form.cleaned_data.get("universidade")
            )

            return redirect("login")

        return render(
            request,
            "cadastro.html",
            {
                "form": form
            }
        )

# =====================================
# PERFIL
# =====================================

class PerfilView(LoginRequiredMixin, View):

    def get(self, request):

        perfil = request.user.perfil

        return render(
            request,
            "perfil.html",
            {
                "perfil": perfil
            }
        )


# =====================================
# EDITAR PERFIL
# =====================================

class EditarPerfilView(LoginRequiredMixin, View):

    def get(self, request):

        perfil = request.user.perfil

        return render(
            request,
            "editar_perfil.html",
            {
                "perfil": perfil
            }
        )

    def post(self, request):

        usuario = request.user

        perfil = usuario.perfil

        usuario.username = request.POST.get("username")

        usuario.email = request.POST.get("email")

        senha = request.POST.get("senha")

        if senha:
            usuario.set_password(senha)

        usuario.save()

        perfil.avatar = request.POST.get("avatar")

        perfil.universidade = request.POST.get("universidade")

        if request.FILES.get("foto"):
            perfil.foto = request.FILES.get("foto")

        perfil.save()

        return redirect("perfil")


# =====================================
# UNIVERSIDADES
# =====================================

class UniversidadesView(LoginRequiredMixin, View):

    def get(self, request):

        universidades = Universidade.objects.all()

        return render(
            request,
            "universidade.html",
            {
                "universidades": universidades
            }
        )


# =====================================
# COMPETIÇÕES
# =====================================

class CompeticoesView(LoginRequiredMixin, View):

    def get(self, request):

        competicoes = Competicao.objects.all()

        form = CompeticaoForm()

        return render(
            request,
            "competicao.html",
            {
                "competicoes": competicoes,
                "form": form
            }
        )

    def post(self, request):

        if not request.user.is_staff:
            return redirect("competicoes")

        form = CompeticaoForm(request.POST)

        if form.is_valid():

            competicao = form.save(commit=False)

            competicao.usuario = request.user

            competicao.save()

        return redirect("competicoes")


# =====================================
# EDITAR COMPETIÇÃO
# =====================================

class EditarCompeticaoView(LoginRequiredMixin, View):

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
            "editar_competicao.html",
            {
                "form": form
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

            obj = form.save(commit=False)

            obj.usuario = competicao.usuario

            obj.save()

            return redirect("competicoes")

        return render(
            request,
            "editar_competicao.html",
            {
                "form": form
            }
        )


# =====================================
# EXCLUIR COMPETIÇÃO
# =====================================

class DeleteCompeticaoView(LoginRequiredMixin, View):

    def get(self, request, id):

        competicao = get_object_or_404(
            Competicao,
            id=id
        )

        competicao.delete()

        return redirect("competicoes")


# =====================================
# RESULTADOS
# =====================================

class ResultadosView(LoginRequiredMixin, View):

    def get(self, request):

        resultados = Resultado.objects.all()

        return render(
            request,
            "resultado.html",
            {
                "resultados": resultados
            }
        )


# =====================================
# CALENDÁRIOS
# =====================================

class CalendariosView(LoginRequiredMixin, View):

    def get(self, request):

        calendarios = Calendario.objects.all()

        return render(
            request,
            "calendario.html",
            {
                "calendarios": calendarios
            }
        )


# =====================================
# NOTIFICAÇÕES
# =====================================

class NotificacoesView(LoginRequiredMixin, View):

    def get(self, request):

        notificacoes = Notificacao.objects.filter(
            usuario=request.user
        )

        return render(
            request,
            "notificacao.html",
            {
                "notificacoes": notificacoes
            }
        )


# =====================================
# FAVORITOS
# =====================================

class FavoritosView(LoginRequiredMixin, View):

    def get(self, request):

        favoritos = Favorito.objects.filter(
            usuario=request.user
        )

        return render(
            request,
            "favoritos.html",
            {
                "favoritos": favoritos
            }
        )


# =====================================
# HISTÓRICO
# =====================================

class HistoricosView(LoginRequiredMixin, View):

    def get(self, request):

        historicos = Historico.objects.filter(
            usuario=request.user
        )

        return render(
            request,
            "historicos.html",
            {
                "historicos": historicos
            }
        )


# =====================================
# PESQUISA
# =====================================

class PesquisaView(LoginRequiredMixin, View):

    def get(self, request):

        pesquisa = request.GET.get("pesquisa", "")

        competicoes = Competicao.objects.all()

        if pesquisa:

            competicoes = competicoes.filter(
                nome__icontains=pesquisa
            )

        return render(
            request,
            "pesquisa.html",
            {
                "competicoes": competicoes,
                "pesquisa": pesquisa
            }
        )