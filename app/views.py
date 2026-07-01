from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .forms import CompeticaoForm, CadastroForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import (
    Competicao, Universidade, Resultado, Calendario, Favorito, Historico,
    Notificacao, Perfil, Administracao, Pessoa
)
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
import json


# =========================
# FUNÇÕES AUXILIARES DE NOTIFICAÇÃO
# =========================
 
def criar_notificacoes_competicao(user, competicao):
    """
    Cria notificações automáticas para 1 mês, 15 dias e 1 semana antes
    da competição
    """
    data_competicao = competicao.data
    hoje = timezone.now().date()
    
    # Notificação: 1 Mês antes
    data_1_mes = data_competicao - timedelta(days=30)
    if data_1_mes >= hoje:
        Notificacao.objects.get_or_create(
            usuario=user,
            competicao=competicao,
            tipo='1_mes',
            defaults={
                'mensagem': f'🗓️ Faltam 1 mês para "{competicao.nome}"',
                'data_agendada': timezone.make_aware(
                    timezone.datetime.combine(data_1_mes, timezone.datetime.min.time())
                ),
                'status': 'pendente'
            }
        )
    
    # Notificação: 15 Dias antes
    data_15_dias = data_competicao - timedelta(days=15)
    if data_15_dias >= hoje:
        Notificacao.objects.get_or_create(
            usuario=user,
            competicao=competicao,
            tipo='15_dias',
            defaults={
                'mensagem': f'⏰ Faltam 15 dias para "{competicao.nome}"',
                'data_agendada': timezone.make_aware(
                    timezone.datetime.combine(data_15_dias, timezone.datetime.min.time())
                ),
                'status': 'pendente'
            }
        )
    
    # Notificação: 1 Semana antes
    data_1_semana = data_competicao - timedelta(days=7)
    if data_1_semana >= hoje:
        Notificacao.objects.get_or_create(
            usuario=user,
            competicao=competicao,
            tipo='1_semana',
            defaults={
                'mensagem': f'⏳ Faltam 7 dias para "{competicao.nome}"',
                'data_agendada': timezone.make_aware(
                    timezone.datetime.combine(data_1_semana, timezone.datetime.min.time())
                ),
                'status': 'pendente'
            }
        )
    
    # Notificação: Hoje é o dia!
    if data_competicao == hoje:
        Notificacao.objects.get_or_create(
            usuario=user,
            competicao=competicao,
            tipo='hoje',
            defaults={
                'mensagem': f'🎉 É HOJE! "{competicao.nome}" está acontecendo!',
                'data_agendada': timezone.now(),
                'status': 'pendente'
            }
        )
 
 
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
# CADASTRO  
# =========================

class CadastroView(View):

    def get(self, request):

        form = CadastroForm()

        return render(
            request,
            'cadastro.html',
            {'form': form}
        )

    def post(self, request):

        form = CadastroForm(request.POST)

        if form.is_valid():

            user = form.save()

            Pessoa.objects.create(
                user=user,
                universidade=""
            )

            Perfil.objects.create(
                user=user
            )

            login(request, user)

            return redirect('/')

        return render(
            request,
            'cadastro.html',
            {
                'form': form
            }
        )
    
# =========================
# LOGOUT
# =========================

class LogoutView(View):

    def get(self, request):

        logout(request)

        return redirect('/')
    

# =========================
# PERFIL
# =========================

class PerfilView(View):
    def get(self, request):
        # Contagens reais do usuário logado
        total_favoritos     = 0
        total_notificacoes  = 0
        notif_nao_lidas     = 0
 
        if request.user.is_authenticated:
            total_favoritos    = Favorito.objects.filter(user=request.user).count()
            total_notificacoes = Notificacao.objects.filter(usuario=request.user).count()
            notif_nao_lidas    = Notificacao.objects.filter(
                usuario=request.user
            ).exclude(status='lida').count()
 
        return render(request, 'perfil.html', {
            'total_favoritos':    total_favoritos,
            'total_notificacoes': total_notificacoes,
            'notif_nao_lidas':    notif_nao_lidas,
        })
 
 
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
# CALENDÁRIOS
# =========================

class CalendariosView(View):
    def get(self, request):
        # Garante que todas as competições têm um Calendario associado
        # (conserta competições antigas cadastradas antes dos signals)
        from .models import Calendario as Cal
        for comp in Competicao.objects.all():
            Cal.objects.get_or_create(
                competicao=comp,
                defaults={
                    'dataEvento': comp.data,
                    'horario': 'A definir',
                }
            )

        # Busca todos os calendários ordenados por data (mais próximos primeiro)
        calendarios = (
            Calendario.objects
            .select_related('competicao', 'competicao__universidade')
            .order_by('dataEvento')
        )

        return render(request, 'calendario.html', {'calendarios': calendarios})


# Endpoint AJAX para o auto-refresh do frontend
class CalendariosAjaxView(View):
    def get(self, request):
        calendarios = (
            Calendario.objects
            .select_related('competicao', 'competicao__universidade')
            .order_by('dataEvento')
        )
        data = {
            'total': calendarios.count(),
            'calendarios': [
                {
                    'id':                    cal.id,
                    'dataEvento':            cal.dataEvento.strftime('%d/%m/%Y'),
                    'horario':               cal.horario,
                    'competicao_nome':       cal.competicao.nome,
                    'competicao_local':      cal.competicao.local,
                    'competicao_organizador':cal.competicao.organizador,
                    'universidade':          cal.competicao.universidade.nome
                                             if cal.competicao.universidade else '',
                }
                for cal in calendarios
            ]
        }
        return JsonResponse(data)



# =========================
# NOTIFICAÇÕES
# =========================

class NotificacoesView(View):
    def get(self, request):
        if request.user.is_authenticated:
            notificacoes = Notificacao.objects.filter(usuario=request.user).order_by('-dataEnvio')
        else:
            notificacoes = Notificacao.objects.none()
 
        return render(
            request,
            'notificacao.html',
            {'notificacoes': notificacoes}
        )
 
 
# NOVO: View para marcar notificação como lida (AJAX)
class MarcarNotificacaoLidaView(LoginRequiredMixin, View):
    def post(self, request, notificacao_id):
        """Marca uma notificação como lida"""
        notificacao = get_object_or_404(Notificacao, id=notificacao_id, usuario=request.user)
        notificacao.marcar_como_lida()
        return JsonResponse({'status': 'lida', 'message': 'Notificação marcada como lida'})
 
 
# =========================
# FAVORITOS (CORRIGIDO COM NOTIFICAÇÕES)
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
 
 
# NOVO: View para adicionar/remover favoritos (AJAX) COM NOTIFICAÇÕES
class ToggleFavoritoView(LoginRequiredMixin, View):
    def post(self, request, competicao_id):
        """Adiciona ou remove um favorito e cria notificações automáticas"""
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Não autenticado'}, status=401)
        
        competicao = get_object_or_404(Competicao, id=competicao_id)
        
        # Tenta encontrar o favorito existente
        favorito = Favorito.objects.filter(user=request.user, competicao=competicao).first()
        
        if favorito:
            # Se existe, remove
            favorito.delete()
            # Remove as notificações associadas também
            Notificacao.objects.filter(
                usuario=request.user,
                competicao=competicao
            ).delete()
            return JsonResponse({
                'status': 'removido',
                'message': 'Removido dos favoritos',
                'is_favorito': False
            })
        else:
            # Se não existe, adiciona
            Favorito.objects.create(user=request.user, competicao=competicao)
            
            # Criar notificação de que foi adicionado aos favoritos
            Notificacao.objects.create(
                usuario=request.user,
                competicao=competicao,
                tipo='favorito_adicionado',
                mensagem=f'💚 Você adicionou "{competicao.nome}" aos favoritos!',
                status='enviada'
            )
            
            # Criar notificações automáticas para 1 mês, 15 dias e 1 semana
            criar_notificacoes_competicao(request.user, competicao)
            
            return JsonResponse({
                'status': 'adicionado',
                'message': 'Adicionado aos favoritos com notificações automáticas!',
                'is_favorito': True
            })
 
 
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