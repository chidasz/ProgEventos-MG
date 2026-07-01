from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [

    # Django Admin
    path('admin/', admin.site.urls),

    # Página Inicial
    path('', IndexView.as_view(), name='index'),

    # Usuário
    path('login/', LoginView.as_view(), name='login'),
    path('perfil/', PerfilView.as_view(), name='perfil'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Competições
    path('competicoes/', CompeticoesView.as_view(), name='competicoes'),
    path(
        'competicao/delete/<int:id>/',
        DeleteCompeticaoView.as_view(),
        name='delete_competicao'
    ),
    path(
        'competicao/editar/<int:id>/',
        EditarCompeticaoView.as_view(),
        name='editar_competicao'
    ),

    # Universidades
    path(
        'universidades/',
        UniversidadesView.as_view(),
        name='universidades'
    ),

    # Resultados
    path(
        'resultados/',
        ResultadosView.as_view(),
        name='resultados'
    ),

    # Calendário
    path(
        'calendarios/',
        CalendariosView.as_view(),
        name='calendarios'
    ),
    # Endpoint AJAX para auto-refresh do calendário
    path(
        'api/calendarios/',
        CalendariosAjaxView.as_view(),
        name='calendarios_ajax'
    ),

    # Notificações
    path(
        'notificacoes/',
        NotificacoesView.as_view(),
        name='notificacoes'
    ),
      path(
        'notificacao/marcar-lida/<int:notificacao_id>/',
        MarcarNotificacaoLidaView.as_view(),
        name='marcar_notificacao_lida'
    ),

    # Favoritos
    path(
        'favoritos/',
        FavoritosView.as_view(),
        name='favoritos'
    ),

    # NOVO: Toggle Favorito (AJAX)
    path(
        'favorito/toggle/<int:competicao_id>/',
        ToggleFavoritoView.as_view(),
        name='toggle_favorito'
    ),

    # Histórico
    path(
        'historicos/',
        HistoricosView.as_view(),
        name='historicos'
    ),

    # Pesquisa
    path(
        'pesquisa/',
        PesquisaView.as_view(),
        name='pesquisa'
    ),

    # Administração
    path(
        'administracoes/',
        AdministracoesView.as_view(),
        name='administracoes'
    ),

    path(
    'cadastro/',
    CadastroView.as_view(),
    name='cadastro'
    ),

]