from django.contrib import admin
from .models import (
    Pessoa, Administracao, Universidade, Competicao, 
    Resultado, Calendario, Notificacao, Perfil, Favorito, Historico, Pesquisa
)


# =========================
# PESSOA
# =========================

@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'universidade')
    list_filter = ('universidade',)
    search_fields = ('user__username', 'universidade')
    readonly_fields = ('id',)


# =========================
# ADMINISTRAÇÃO
# =========================

@admin.register(Administracao)
class AdministracaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'nivelAcesso', 'universidade')
    list_filter = ('nivelAcesso',)
    search_fields = ('user__username', 'nivelAcesso')
    readonly_fields = ('id',)


# =========================
# UNIVERSIDADE
# =========================

@admin.register(Universidade)
class UniversidadeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sigla', 'cidade')
    list_filter = ('cidade',)
    search_fields = ('nome', 'sigla', 'cidade')
    readonly_fields = ('id',)


# =========================
# COMPETIÇÃO
# =========================

@admin.register(Competicao)
class CompeticaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'data', 'universidade', 'organizador')
    list_filter = ('data', 'universidade', 'organizador')
    search_fields = ('nome', 'descricao', 'organizador')
    readonly_fields = ('id',)
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'data')
        }),
        ('Localização', {
            'fields': ('local', 'universidade')
        }),
        ('Gestão', {
            'fields': ('organizador', 'pessoa', 'administrador')
        }),
    )
    date_hierarchy = 'data'


# =========================
# RESULTADO (CORRIGIDO - Sem campo colocacao)
# =========================

@admin.register(Resultado)
class ResultadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'equipe', 'get_colocacao', 'pontuacao', 'competicao')
    list_filter = ('competicao', 'pontuacao')
    search_fields = ('equipe', 'competicao__nome')
    readonly_fields = ('id', 'get_colocacao', 'criado_em', 'atualizado_em')
    fieldsets = (
        ('Informações da Equipe', {
            'fields': ('equipe', 'competicao')
        }),
        ('Desempenho', {
            'fields': ('pontuacao', 'get_colocacao')
        }),
        ('Auditoria', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def get_colocacao(self, obj):
        """Exibe a colocação calculada dinamicamente"""
        return f"{obj.colocacao}º lugar"
    get_colocacao.short_description = "Colocação"
    
    def get_readonly_fields(self, request, obj=None):
        """Deixa pontuacao editável apenas na criação"""
        if obj:
            return self.readonly_fields + ('pontuacao',)
        return self.readonly_fields


# =========================
# CALENDÁRIO
# =========================

@admin.register(Calendario)
class CalendarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'dataEvento', 'horario', 'competicao')
    list_filter = ('dataEvento',)
    search_fields = ('competicao__nome', 'horario')
    readonly_fields = ('id',)
    date_hierarchy = 'dataEvento'
    fieldsets = (
        ('Informações do Evento', {
            'fields': ('dataEvento', 'horario')
        }),
        ('Competição Associada', {
            'fields': ('competicao',)
        }),
    )


# =========================
# NOTIFICAÇÃO
# =========================

@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'mensagem', 'dataEnvio', 'pessoa')
    list_filter = ('dataEnvio',)
    search_fields = ('mensagem', 'pessoa__user__username')
    readonly_fields = ('id', 'dataEnvio')
    date_hierarchy = 'dataEnvio'


# =========================
# PERFIL
# =========================

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'universidade')
    list_filter = ('universidade',)
    search_fields = ('user__username', 'universidade')
    readonly_fields = ('id',)
    fieldsets = (
        ('Usuário', {
            'fields': ('user',)
        }),
        ('Informações Pessoais', {
            'fields': ('universidade', 'descricao', 'foto')
        }),
    )


# =========================
# FAVORITO
# =========================

@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'competicao', 'criado_em')
    list_filter = ('criado_em', 'user')
    search_fields = ('user__username', 'competicao__nome')
    readonly_fields = ('id', 'criado_em')
    date_hierarchy = 'criado_em'
    fieldsets = (
        ('Favorito', {
            'fields': ('user', 'competicao')
        }),
        ('Auditoria', {
            'fields': ('criado_em',),
            'classes': ('collapse',)
        }),
    )


# =========================
# HISTÓRICO
# =========================

@admin.register(Historico)
class HistoricoAdmin(admin.ModelAdmin):
    list_display = ('id', 'equipe', 'data', 'get_posicao', 'pessoa')
    list_filter = ('data',)
    search_fields = ('equipe', 'pessoa__user__username')
    readonly_fields = ('id',)

    fieldsets = (
        ('Informações', {
            'fields': ('equipe', 'data')
        }),
        ('Pessoa', {
            'fields': ('pessoa',)
        }),
        ('Resultado', {
            'fields': ('resultado',)
        }),
    )

    def get_posicao(self, obj):
        return obj.resultado.colocacao if obj.resultado else None

    get_posicao.short_description = 'Posição'


# =========================
# PESQUISA
# =========================

@admin.register(Pesquisa)
class PesquisaAdmin(admin.ModelAdmin):
    list_display = ('id', 'modalidade', 'cidade', 'universidade')
    list_filter = ('modalidade', 'cidade', 'universidade')
    search_fields = ('modalidade', 'cidade', 'universidade')
    readonly_fields = ('id',)
    fieldsets = (
        ('Filtros de Busca', {
            'fields': ('cidade', 'universidade', 'modalidade')
        }),
    )


# =========================
# CONFIGURAÇÕES GLOBAIS DO ADMIN
# =========================

admin.site.site_header = "ProgEventos-MG - Administração"
admin.site.site_title = "ProgEventos-MG Admin"
admin.site.index_title = "Bem-vindo ao painel administrativo"
