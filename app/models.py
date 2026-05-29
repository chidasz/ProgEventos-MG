from django.db import models


class Pessoa(models.Model):
    nome = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    senha = models.CharField(max_length=50)
    universidade = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Administracao(Pessoa):
    nivelAcesso = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nome} - Administrador"


class Universidade(models.Model):
    nome = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    sigla = models.CharField(max_length=20)

    def __str__(self):
        return self.nome


class Competicao(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=200)
    data = models.DateField()
    local = models.CharField(max_length=100)
    organizador = models.CharField(max_length=100)

    pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.CASCADE,
        related_name="competicoes"
    )

    universidade = models.ForeignKey(
        Universidade,
        on_delete=models.CASCADE,
        related_name="competicoes"
    )

    administrador = models.ForeignKey(
        Administracao,
        on_delete=models.CASCADE,
        related_name="competicoes_gerenciadas"
    )

    def __str__(self):
        return self.nome


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
        return f"{self.equipe} - {self.colocacao}º lugar"


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


class Notificacao(models.Model):
    mensagem = models.CharField(max_length=200)
    dataEnvio = models.DateField()

    pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.CASCADE,
        related_name="notificacoes"
    )

    def __str__(self):
        return self.mensagem