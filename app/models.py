from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone


class Pessoa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    universidade = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username if self.user else 'Pessoa'}"


class Administracao(Pessoa):
    nivelAcesso = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username} - Administrador" if self.user else "Administrador"


class Universidade(models.Model):
    nome = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    sigla = models.CharField(max_length=20)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Universidades"


class Competicao(models.Model):
    nome        = models.CharField(max_length=100)
    descricao   = models.CharField(max_length=1000)
    data        = models.DateField()
    local       = models.CharField(max_length=100)
    organizador = models.CharField(max_length=100)

    pessoa = models.ForeignKey(
        Pessoa, on_delete=models.CASCADE,
        related_name='competicoes', null=True, blank=True
    )
    universidade = models.ForeignKey(
        Universidade, on_delete=models.CASCADE,
        related_name='competicoes', null=True, blank=True
    )
    administrador = models.ForeignKey(
        Administracao, on_delete=models.CASCADE,
        related_name='competicoes_gerenciadas', null=True, blank=True
    )

    # null=True garante que a migration roda sem quebrar linhas existentes
    criado_em = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Competições"
        ordering = ['-data']


class Resultado(models.Model):
    equipe    = models.CharField(max_length=100)
    pontuacao = models.FloatField()

    competicao = models.ForeignKey(
        Competicao, on_delete=models.CASCADE, related_name='resultados'
    )
    criado_em     = models.DateTimeField(auto_now_add=True, null=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    @property
    def colocacao(self):
        ids = list(
            Resultado.objects
            .filter(competicao=self.competicao)
            .order_by('-pontuacao')
            .values_list('id', flat=True)
        )
        try:
            return ids.index(self.id) + 1
        except ValueError:
            return None

    def __str__(self):
        return f"{self.equipe} - {self.pontuacao} pts"

    class Meta:
        verbose_name_plural = "Resultados"
        ordering = ['-pontuacao']


class Calendario(models.Model):
    dataEvento = models.DateField()
    horario    = models.CharField(max_length=20)

    competicao = models.OneToOneField(
        Competicao, on_delete=models.CASCADE, related_name='calendario'
    )

    def __str__(self):
        return f"{self.dataEvento} - {self.horario}"

    class Meta:
        verbose_name_plural = "Calendários"
        ordering = ['dataEvento']


class Notificacao(models.Model):
    TIPOS = [
        ('favorito_adicionado', 'Favorito Adicionado'),
        ('1_mes',    'Faltam 1 Mês'),
        ('15_dias',  'Faltam 15 Dias'),
        ('1_semana', 'Falta 1 Semana'),
        ('hoje',     'É Hoje!'),
    ]
    STATUS = [
        ('pendente', 'Pendente'),
        ('enviada',  'Enviada'),
        ('lida',     'Lida'),
    ]

    mensagem   = models.CharField(max_length=500)
    dataEnvio  = models.DateTimeField(auto_now_add=True)

    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='notificacoes_usuario', null=True, blank=True
    )
    pessoa = models.ForeignKey(
        Pessoa, on_delete=models.CASCADE,
        related_name='notificacoes', null=True, blank=True
    )
    competicao = models.ForeignKey(
        Competicao, on_delete=models.CASCADE,
        related_name='notificacoes', null=True, blank=True
    )

    tipo           = models.CharField(max_length=20, choices=TIPOS, default='favorito_adicionado')
    status         = models.CharField(max_length=20, choices=STATUS, default='pendente')
    data_agendada  = models.DateTimeField(null=True, blank=True)
    lida_em        = models.DateTimeField(null=True, blank=True)

    def marcar_como_lida(self):
        self.status  = 'lida'
        self.lida_em = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.mensagem} [{self.status}]"

    class Meta:
        verbose_name_plural = "Notificações"
        ordering = ['-dataEnvio']


class Perfil(models.Model):
    user         = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    universidade = models.CharField(max_length=100, blank=True, null=True)
    foto         = models.ImageField(upload_to='perfil/', blank=True, null=True)
    descricao    = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.user.username}" if self.user else "Perfil"


class Favorito(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='favoritos', null=True, blank=True
    )
    competicao = models.ForeignKey(
        Competicao, on_delete=models.CASCADE, related_name='favoritado_por'
    )
    criado_em = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        u = self.user.username if self.user else "?"
        return f"{u} ❤ {self.competicao.nome}"

    class Meta:
        verbose_name_plural = "Favoritos"
        unique_together = ('user', 'competicao')
        ordering = ['-criado_em']


class Historico(models.Model):
    data      = models.DateField()
    equipe    = models.CharField(max_length=100)
    pessoa    = models.ForeignKey(Pessoa,    on_delete=models.CASCADE)
    resultado = models.ForeignKey(Resultado, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.equipe} ({self.data})"


class Pesquisa(models.Model):
    cidade       = models.CharField(max_length=100)
    universidade = models.CharField(max_length=100)
    modalidade   = models.CharField(max_length=100)

    def __str__(self):
        return self.modalidade

    class Meta:
        verbose_name_plural = "Pesquisas"