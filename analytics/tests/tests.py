from django.test import TestCase
from analytics.models import Prova, Aluno
from django.db import models

# Create your tests here.

class TestApproval(TestCase):
    def test_is_approved(self):
        aluno = Aluno(
            nome = "Mario Cirilo",
        )
        aluno.save()
        prova = Prova(
            aluno = aluno,
            nota = 6, 
        )
        if prova.nota >= 6:
            prova.aprovado = True
        prova.save()
        
        self.assertEqual(Prova.objects.get(id=aluno.id).aprovado, True)