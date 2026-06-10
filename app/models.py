from django.db import models
from django.contrib.auth.models import User


# =========================
# PESSOA
# =========================

class Pessoa(models.Model):
    nome = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    senha = models.CharField(max_length=50)
    universidade = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


# =========================
# ADMINISTRAÇÃO
# =========================

class Administracao(Pessoa):
    nivelAcesso = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nome} - Administrador"


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
    descricao = models.CharField(max_length=1000)
    data = models.DateField()
    local = models.CharField(max_length=100)
    organizador = models.CharField(max_length=100)

    pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.CASCADE,
        related_name='competicoes'
    )

    universidade = models.ForeignKey(
        Universidade,
        on_delete=models.CASCADE,
        related_name='competicoes'
    )

    administrador = models.ForeignKey(
        Administracao,
        on_delete=models.CASCADE,
        related_name='competicoes_gerenciadas'
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
        related_name='resultados'
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
        related_name='calendario'
    )

    def __str__(self):
        return f"{self.dataEvento} - {self.horario}"


# =========================
# NOTIFICAÇÃO
# =========================

class Notificacao(models.Model):
    mensagem = models.CharField(max_length=200)
    dataEnvio = models.DateField()

    pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.CASCADE,
        related_name='notificacoes'
    )

    def __str__(self):
        return self.mensagem


# =========================
# PERFIL
# =========================

class Perfil(models.Model):
    pessoa = models.OneToOneField(
        Pessoa,
        on_delete=models.CASCADE
    )

    foto = models.ImageField(
        upload_to='perfil/',
        blank=True,
        null=True
    )

    descricao = models.TextField()

    def __str__(self):
        return self.pessoa.nome


# =========================
# FAVORITOS
# =========================

class Favorito(models.Model):
    pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.CASCADE
    )

    competicao = models.ForeignKey(
        Competicao,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.pessoa.nome} - {self.competicao.nome}"


# =========================
# HISTÓRICO
# =========================

class Historico(models.Model):
    ano = models.IntegerField()
    equipe = models.CharField(max_length=100)
    posicao = models.IntegerField()

    pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.CASCADE
    )

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