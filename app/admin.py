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
    list_display = ('id', 'nome', 'data', 'universidade', 'organizador', 'get_total_favoritos')
    list_filter = ('data', 'universidade', 'organizador', 'criado_em')
    search_fields = ('nome', 'descricao', 'organizador')
    readonly_fields = ('id', 'criado_em', 'get_total_favoritos')
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
        ('Auditoria', {
            'fields': ('criado_em',),
            'classes': ('collapse',)
        }),
    )
    date_hierarchy = 'data'
    
    def get_total_favoritos(self, obj):
        """Mostra quantos usuários favoritaram"""
        total = Favorito.objects.filter(competicao=obj).count()
        return f"❤️ {total} favorito(s)"
    get_total_favoritos.short_description = "Favoritos"


# =========================
# RESULTADO
# =========================

@admin.register(Resultado)
class ResultadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'equipe', 'get_colocacao', 'pontuacao', 'competicao')
    list_filter = ('competicao', 'pontuacao', 'criado_em')
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
    get_colocacao.short_description = "Colocação (Calculada)"


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
# NOTIFICAÇÃO (MELHORADO)
# =========================

@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_icon', 'mensagem', 'usuario', 'tipo', 'status', 'dataEnvio')
    list_filter = ('tipo', 'status', 'dataEnvio', 'data_agendada')
    search_fields = ('mensagem', 'usuario__username', 'competicao__nome')
    readonly_fields = ('id', 'dataEnvio', 'get_icon')
    fieldsets = (
        ('Notificação', {
            'fields': ('mensagem', 'tipo', 'get_icon')
        }),
        ('Destinatário', {
            'fields': ('usuario', 'competicao')
        }),
        ('Status', {
            'fields': ('status', 'lida_em')
        }),
        ('Agendamento', {
            'fields': ('data_agendada', 'dataEnvio'),
            'classes': ('collapse',)
        }),
    )
    date_hierarchy = 'dataEnvio'
    
    def get_icon(self, obj):
        """Mostra ícone do tipo de notificação"""
        icons = {
            'favorito_adicionado': '💚 Favorito',
            '1_mes': '📅 1 Mês',
            '15_dias': '⏰ 15 Dias',
            '1_semana': '⏳ 1 Semana',
            'hoje': '🎉 Hoje'
        }
        return icons.get(obj.tipo, obj.tipo)
    get_icon.short_description = "Tipo"
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            # Quando editando, deixa alguns campos readonly
            return self.readonly_fields + ('dataEnvio',)
        return self.readonly_fields


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
# FAVORITO (COM NOTIFICAÇÕES)
# =========================

@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'competicao', 'get_dias_restantes', 'criado_em')
    list_filter = ('criado_em', 'user', 'competicao__data')
    search_fields = ('user__username', 'competicao__nome')
    readonly_fields = ('id', 'criado_em', 'get_dias_restantes', 'get_notificacoes')
    date_hierarchy = 'criado_em'
    fieldsets = (
        ('Favorito', {
            'fields': ('user', 'competicao')
        }),
        ('Detalhes', {
            'fields': ('get_dias_restantes', 'get_notificacoes')
        }),
        ('Auditoria', {
            'fields': ('criado_em',),
            'classes': ('collapse',)
        }),
    )
    
    def get_dias_restantes(self, obj):
        """Mostra quantos dias faltam para a competição"""
        from datetime import date
        dias = (obj.competicao.data - date.today()).days
        if dias > 0:
            return f"⏳ Faltam {dias} dias"
        elif dias == 0:
            return "🎉 É HOJE!"
        else:
            return f"✅ Passou há {abs(dias)} dias"
    get_dias_restantes.short_description = "Status"
    
    def get_notificacoes(self, obj):
        """Mostra notificações associadas"""
        notifs = Notificacao.objects.filter(
            usuario=obj.user,
            competicao=obj.competicao
        ).count()
        return f"🔔 {notifs} notificação(ões)"
    get_notificacoes.short_description = "Notificações"


# =========================
# HISTÓRICO
# =========================

@admin.register(Historico)
class HistoricoAdmin(admin.ModelAdmin):
    list_display = ('id', 'equipe', 'data', 'pessoa', 'resultado')
    list_filter = ('data', 'pessoa')
    search_fields = ('equipe', 'pessoa__user__username')
    readonly_fields = ('id',)
    date_hierarchy = 'data'
    fieldsets = (
        ('Informações', {
            'fields': ('equipe', 'data', 'resultado')
        }),
        ('Pessoa', {
            'fields': ('pessoa',)
        }),
    )


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

admin.site.site_header = "ProgEventos-MG - Administração v3.0"
admin.site.site_title = "ProgEventos-MG Admin"
admin.site.index_title = "Painel Administrativo - Favoritos e Notificações"
