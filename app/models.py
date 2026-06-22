from django.db import models
from django.contrib.auth.models import User


# =========================
# PESSOA
# =========================

class Pessoa(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    universidade = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username if self.user else 'Pessoa'}"


# =========================
# ADMINISTRAÇÃO
# =========================

class Administracao(Pessoa):
    nivelAcesso = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username} - Administrador" if self.user else "Administrador"


# =========================
# UNIVERSIDADE
# =========================

class Universidade(models.Model):
    nome = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    sigla = models.CharField(max_length=20)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name_plural = "Universidades"


# =========================
# COMPETIÇÃO
# =========================

class Competicao(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=1000)
    data = models.DateField()
    local = models.CharField(max_length=100)
    organizador = models.CharField(max_length=100)

    pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.CASCADE,
        related_name='competicoes',
        null=True,
        blank=True
    )

    universidade = models.ForeignKey(
        Universidade,
        on_delete=models.CASCADE,
        related_name='competicoes',
        null=True,
        blank=True
    )

    administrador = models.ForeignKey(
        Administracao,
        on_delete=models.CASCADE,
        related_name='competicoes_gerenciadas',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name_plural = "Competições"
        ordering = ['-data']


# =========================
# RESULTADO (CORRIGIDO - Removido campo colocacao)
# =========================

class Resultado(models.Model):
    equipe = models.CharField(max_length=100)
    # REMOVIDO: colocacao = models.IntegerField()
    # MANTIDO: apenas pontuacao - colocação será calculada automaticamente
    pontuacao = models.FloatField()

    competicao = models.ForeignKey(
        Competicao,
        on_delete=models.CASCADE,
        related_name='resultados'
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.equipe} - {self.pontuacao} pts"
    
    @property
    def colocacao(self):
        """Calcula a colocação dinamicamente com base na pontuação"""
        resultados_mesma_competicao = Resultado.objects.filter(
            competicao=self.competicao
        ).order_by('-pontuacao').values_list('id', flat=True)
        
        try:
            return list(resultados_mesma_competicao).index(self.id) + 1
        except ValueError:
            return None
    
    class Meta:
        verbose_name_plural = "Resultados"
        ordering = ['-pontuacao']
        unique_together = ('competicao', 'equipe')


# =========================
# CALENDÁRIO
# =========================

class Calendario(models.Model):
    dataEvento = models.DateField()
    horario = models.CharField(max_length=20)

    competicao = models.OneToOneField(
        Competicao,
        on_delete=models.CASCADE,
        related_name='calendario'
    )

    def __str__(self):
        return f"{self.dataEvento} - {self.horario}"
    
    class Meta:
        verbose_name_plural = "Calendários"
        ordering = ['-dataEvento']


# =========================
# NOTIFICAÇÃO
# =========================

class Notificacao(models.Model):
    mensagem = models.CharField(max_length=200)
    dataEnvio = models.DateField(auto_now_add=True)

    pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.CASCADE,
        related_name='notificacoes',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.mensagem
    
    class Meta:
        verbose_name_plural = "Notificações"
        ordering = ['-dataEnvio']


# =========================
# PERFIL
# =========================

class Perfil(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    universidade = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    foto = models.ImageField(
        upload_to='perfil/',
        blank=True,
        null=True
    )

    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.user.username}" if self.user else "Perfil"


# =========================
# FAVORITOS
# =========================

class Favorito(models.Model):
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='favoritos'
    )

    competicao = models.ForeignKey(
        Competicao,
        on_delete=models.CASCADE,
        related_name='favoritado_por'
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.competicao.nome}" if self.user else f"Favorito - {self.competicao.nome}"
    
    class Meta:
        verbose_name_plural = "Favoritos"
        unique_together = ('user', 'competicao')
        ordering = ['-criado_em']


# =========================
# HISTÓRICO
# =========================

class Historico(models.Model):
    data = models.DateField()
    equipe = models.CharField(max_length=100)

    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    resultado = models.ForeignKey(Resultado, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.equipe} ({self.data}) - {self.resultado.colocacao}º"


# =========================
# PESQUISA
# =========================

class Pesquisa(models.Model):
    cidade = models.CharField(max_length=100)
    universidade = models.CharField(max_length=100)
    modalidade = models.CharField(max_length=100)

    def __str__(self):
        return self.modalidade
    
    class Meta:
        verbose_name_plural = "Pesquisas"
