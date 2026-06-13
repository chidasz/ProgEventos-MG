from django.db import models
from django.contrib.auth.models import User


# =========================
# PERFIL
# =========================

class Perfil(models.Model):

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="perfil"
    )

    foto = models.ImageField(
        upload_to="perfil/",
        blank=True,
        null=True
    )

    avatar = models.CharField(
        max_length=20,
        choices=[
            ("homem", "Homem"),
            ("mulher", "Mulher"),
            ("neutro", "Neutro"),
        ],
        default="neutro"
    )

    universidade = models.CharField(
        max_length=100,
        blank=True
    )

    def __str__(self):
        return self.usuario.username


# =========================
# UNIVERSIDADE
# =========================

class Universidade(models.Model):

    nome = models.CharField(max_length=100)

    cidade = models.CharField(max_length=100)

    sigla = models.CharField(max_length=20)

    def __str__(self):
        return self.nome


# =========================
# COMPETIÇÃO
# =========================

class Competicao(models.Model):

    nome = models.CharField(max_length=100)

    descricao = models.TextField()

    data = models.DateField()

    local = models.CharField(max_length=100)

    organizador = models.CharField(max_length=100)

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="competicoes"
    )

    universidade = models.ForeignKey(
        Universidade,
        on_delete=models.CASCADE,
        related_name="competicoes"
    )

    def __str__(self):
        return self.nome


# =========================
# RESULTADO
# =========================

class Resultado(models.Model):

    equipe = models.CharField(max_length=100)

    colocacao = models.IntegerField()

    pontuacao = models.FloatField()

    competicao = models.ForeignKey(
        Competicao,
        on_delete=models.CASCADE,
        related_name="resultados"
    )

    def __str__(self):
        return f"{self.equipe} - {self.colocacao}º Lugar"


# =========================
# CALENDÁRIO
# =========================

class Calendario(models.Model):

    dataEvento = models.DateField()

    horario = models.CharField(max_length=20)

    competicao = models.OneToOneField(
        Competicao,
        on_delete=models.CASCADE,
        related_name="calendario"
    )

    def __str__(self):
        return f"{self.dataEvento} - {self.horario}"


# =========================
# NOTIFICAÇÃO
# =========================

class Notificacao(models.Model):

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notificacoes"
    )

    mensagem = models.CharField(max_length=200)

    dataEnvio = models.DateField()

    def __str__(self):
        return self.mensagem


# =========================
# FAVORITOS
# =========================

class Favorito(models.Model):

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favoritos"
    )

    competicao = models.ForeignKey(
        Competicao,
        on_delete=models.CASCADE,
        related_name="favoritado_por"
    )

    def __str__(self):
        return f"{self.usuario.username} - {self.competicao.nome}"


# =========================
# HISTÓRICO
# =========================

class Historico(models.Model):

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="historicos"
    )

    ano = models.IntegerField()

    equipe = models.CharField(max_length=100)

    posicao = models.IntegerField()

    def __str__(self):
        return f"{self.equipe} ({self.ano})"


# =========================
# PESQUISA
# =========================

class Pesquisa(models.Model):

    cidade = models.CharField(max_length=100)

    universidade = models.CharField(max_length=100)

    modalidade = models.CharField(max_length=100)

    def __str__(self):
        return self.modalidade