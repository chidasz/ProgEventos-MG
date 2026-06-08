from django.contrib import admin
from .models import *


# INLINE → Resultado dentro de Competicao
class ResultadoInline(admin.TabularInline):
    model = Resultado
    extra = 1


# CUSTOMIZAÇÃO DO ADMIN DE COMPETIÇÃO
class CompeticaoAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'data',
        'local',
        'organizador'
    )

    search_fields = (
        'nome',
        'organizador',
        'local'
    )

    list_filter = (
        'data',
        'local'
    )

    inlines = [
        ResultadoInline
    ]


# CUSTOMIZAÇÃO DO ADMIN DE PESSOA
class PessoaAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'email',
        'universidade'
    )

    search_fields = (
        'nome',
        'email'
    )


# CUSTOMIZAÇÃO DO ADMIN DE UNIVERSIDADE
class UniversidadeAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'cidade',
        'sigla'
    )

    search_fields = (
        'nome',
        'cidade',
        'sigla'
    )


# REGISTROS
admin.site.register(Pessoa, PessoaAdmin)
admin.site.register(Administracao)
admin.site.register(Universidade, UniversidadeAdmin)
admin.site.register(Competicao, CompeticaoAdmin)
admin.site.register(Resultado)
admin.site.register(Calendario)
admin.site.register(Notificacao)
admin.site.register(Perfil)
admin.site.register(Favorito)
admin.site.register(Historico)
admin.site.register(Pesquisa)