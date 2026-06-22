from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login
from .forms import CompeticaoForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from .models import (
    Competicao, Universidade, Resultado, Calendario, Favorito, Historico, Notificacao, Perfil, Administracao, Pessoa)
from django.http import JsonResponse
from django.db.models import Q

# =========================
# PÁGINA INICIAL
# =========================

class IndexView(View):

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
# LOGIN (CORRIGIDO - Adicionado GET)
# =========================

class LoginView(View):

    def get(self, request):
        """Exibe o formulário de login"""
        return render(request, "login.html")

    def post(self, request):
        """Processa o login"""
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
        
        # Adiciona se é favorito do usuário logado
        if request.user.is_authenticated:
            favoritos = Favorito.objects.filter(user=request.user).values_list('competicao_id', flat=True)
            for competicao in competicoes:
                competicao.is_favorito = competicao.id in favoritos
        
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


# CORRIGIDO: EditarCompeticaoView com correta renderização
class EditarCompeticaoView(LoginRequiredMixin, View):

    def get(self, request, id):
        competicao = get_object_or_404(Competicao, id=id)
        form = CompeticaoForm(instance=competicao)

        return render(
            request,
            'editar_competicao.html',
            {'form': form, 'competicao': competicao}
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
            {'form': form, 'competicao': competicao}
        )


# =========================
# RESULTADOS (CORRIGIDO)
# =========================

class ResultadosView(View):
    def get(self, request):
        # Busca todos os resultados e ordena por pontuação descrescente
        resultados = Resultado.objects.all().order_by('-pontuacao')
        
        # Agrupa por competição e ordena cada grupo por pontuação
        resultados_por_competicao = {}
        for resultado in resultados:
            comp_id = resultado.competicao.id
            if comp_id not in resultados_por_competicao:
                resultados_por_competicao[comp_id] = {
                    'competicao': resultado.competicao,
                    'resultados': []
                }
            resultados_por_competicao[comp_id]['resultados'].append(resultado)
        
        # Converte para lista para uso no template
        grupos = list(resultados_por_competicao.values())

        return render(
            request,
            'resultado.html',
            {'grupos': grupos, 'resultados': resultados}
        )


# =========================
# CALENDÁRIOS (CORRIGIDO - Ordenado por data)
# =========================

class CalendariosView(View):
    def get(self, request):
        # Ordena calendários por data de evento (decrescente - próximos eventos primeiro)
        calendarios = Calendario.objects.all().order_by('-dataEvento')
        
        # Filtra apenas calendários com competições associadas
        calendarios = calendarios.filter(competicao__isnull=False)

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
# FAVORITOS (CORRIGIDO - Filtra por usuário logado)
# =========================

class FavoritosView(View):
    def get(self, request):
        # Filtra favoritos apenas do usuário logado
        if request.user.is_authenticated:
            favoritos = Favorito.objects.filter(user=request.user)
        else:
            favoritos = Favorito.objects.none()

        return render(
            request,
            'favoritos.html',
            {'favoritos': favoritos}
        )


# NOVO: View para adicionar/remover favoritos (AJAX)
class ToggleFavoritoView(LoginRequiredMixin, View):
    def post(self, request, competicao_id):
        """Adiciona ou remove um favorito"""
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Não autenticado'}, status=401)
        
        competicao = get_object_or_404(Competicao, id=competicao_id)
        
        # Tenta encontrar o favorito existente
        favorito = Favorito.objects.filter(user=request.user, competicao=competicao).first()
        
        if favorito:
            # Se existe, remove
            favorito.delete()
            return JsonResponse({'status': 'removido', 'message': 'Removido dos favoritos'})
        else:
            # Se não existe, adiciona
            Favorito.objects.create(user=request.user, competicao=competicao)
            return JsonResponse({'status': 'adicionado', 'message': 'Adicionado aos favoritos'})


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
                Q(nome__icontains=pesquisa) |
                Q(descricao__icontains=pesquisa) |
                Q(organizador__icontains=pesquisa) |
                Q(universidade__nome__icontains=pesquisa)
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
