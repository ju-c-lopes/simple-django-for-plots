from django.db import models
from django.contrib.auth.models import User

possiveis_notas = [[f"{i}", nota] for i, nota in enumerate(range(11))]

# Create your models here.

class Aluno(models.Model):
    nome = models.TextField(max_length=100, blank=True, null=True)
    notas = models.ManyToManyField('Prova', db_column='pk', blank=True, related_name='prova')

    def __str__(self):
        return f"{self.nome}"

class Prova(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    nota = models.IntegerField(choices=possiveis_notas, default=0)
    aprovado = models.BooleanField(default=False)