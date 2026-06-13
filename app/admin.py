from django.contrib import admin
from .models import *


class ResultadoInline(admin.TabularInline):
    model = Resultado
    extra = 1


class CompeticaoAdmin(admin.ModelAdmin):

    list_display = (
        "nome",
        "data",
        "local",
        "organizador"
    )

    search_fields = (
        "nome",
        "organizador",
        "local"
    )

    list_filter = (
        "data",
        "local"
    )

    inlines = [
        ResultadoInline
    ]


class UniversidadeAdmin(admin.ModelAdmin):

    list_display = (
        "nome",
        "cidade",
        "sigla"
    )

    search_fields = (
        "nome",
        "cidade",
        "sigla"
    )


admin.site.register(Universidade, UniversidadeAdmin)
admin.site.register(Competicao, CompeticaoAdmin)
admin.site.register(Resultado)
admin.site.register(Calendario)
admin.site.register(Notificacao)
admin.site.register(Perfil)
admin.site.register(Favorito)
admin.site.register(Historico)
admin.site.register(Pesquisa)