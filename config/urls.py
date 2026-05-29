from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    # Página inicial
    path('', IndexView.as_view(), name='index'),

    # Listagens
    path('pessoas/', PessoasView.as_view(), name='pessoas'),
    path('administracoes/', AdministracoesView.as_view(), name='administracoes'),
    path('universidades/', UniversidadesView.as_view(), name='universidades'),
    path('competicoes/', CompeticoesView.as_view(), name='competicoes'),
    path('resultados/', ResultadosView.as_view(), name='resultados'),
    path('calendarios/', CalendariosView.as_view(), name='calendarios'),
    path('notificacoes/', NotificacoesView.as_view(), name='notificacoes'),

    # Competições
    path('competicao/delete/<int:id>/', DeleteCompeticaoView.as_view(), name='delete_competicao'),
    path('competicao/editar/<int:id>/', EditarCompeticaoView.as_view(), name='editar_competicao'),
]