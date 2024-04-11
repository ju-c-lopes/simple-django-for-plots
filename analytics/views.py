from django.shortcuts import render, redirect
from django.contrib import messages
from analytics.models import Aluno, Prova, possiveis_notas
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io, base64
import numpy as np

# Create your views here.

def consultar_aluno(request):
    context = None
    aluno = None
    if request.GET:
        try:
            if request.GET.get('consulta', False):
                aluno = Aluno.objects.get(nome__contains=request.GET['consulta'])
        except:
            messages.error(request, 'Aluno não encontrado.')
    context = {
        'aluno': aluno,
    }
    return render(request, template_name='home.html', context=context, status=200)

def registrar_aluno(request):

    if request.POST:
        if request.POST.get('nome', False):
            aluno = Aluno(
                nome = request.POST.get("nome", None)
            )
            aluno.save()
            messages.success(request, 'Aluno(a) registrado com sucesso.')
            return redirect('home')
    return render(request, template_name='registro-aluno.html', status=200)

def registrar_nota(request):
    alunos = None
    if request.POST:
        aprovado = int(request.POST.get("nota", 0)) >= 6
        nota = Prova(
            aluno = Aluno.objects.get(id=request.POST.get("aluno", None)),
            nota = request.POST.get("nota", None),
            aprovado = aprovado,
        )
        nota.save()
        Aluno.objects.get(id=request.POST.get("aluno", None)).notas.add(nota)
        messages.success(request, 'Nota atribuida com sucesso.')
        return redirect('home')
    else:
        alunos = Aluno.objects.all()
    context = {
        'alunos': alunos,
        'notas': possiveis_notas,
    }
    return render(request, template_name='registro-nota.html', context=context, status=200)

def criar_graficos(request):
    context = {}
    notas = None
    selecao_de_alunos = []
    if not request.POST:
        selecao_de_alunos = Aluno.objects.all()
    if request.POST:
        alunos = request.POST.getlist("alunos")
        if 'all' in alunos:
            selecao_de_alunos = Aluno.objects.all()
        else:
            todos_alunos = Aluno.objects.all()
            for i in range(len(todos_alunos)):
                for id_aluno in alunos:
                    if todos_alunos[i].id == int(id_aluno):
                        selecao_de_alunos.append(todos_alunos[i])

        notas = {}
        nomes_alunos = [aluno.nome for aluno in selecao_de_alunos]
        media_alunos = []
        maximo = 9999
        for aluno in selecao_de_alunos:
            notas[f"{aluno.nome}"] = [nota.nota for nota in aluno.notas.all()]
            temp_min = len(aluno.notas.all())
            maximo = temp_min if temp_min < maximo else maximo

        x = np.arange(maximo)
        width = 0.25
        multiplier = 0

        fig, ax = plt.subplots(figsize=(15, 6), layout="constrained")
        for nome, notas in notas.items():
            offset = width * multiplier
            rects = ax.bar(x + offset, notas, width, label=nome)
            ax.bar_label(rects, padding=3)
            multiplier += 1

        # Comentario mantido para tentar outra abordagem
        # ax.plot(
        #     [n.nota 
        #         for nota in notas
        #         for n in nota
        #         ],
        #     [aluno.nome for aluno in selecao_de_alunos],
        #     '--bo')

        ax.set_title('Notas de alunos')
        ax.set_ylabel('Notas')
        ax.set_xticks(x + width, [f"{i + 1}° Nota" for i in range(maximo)])
        ax.legend(loc='upper left', ncols=len(nomes_alunos))
        ax.set_ylim(0, 10)
        
        file_io = io.BytesIO()
        fig.savefig(file_io)
        b64 = base64.b64encode(file_io.getvalue()).decode()
        context['chart'] = b64

    context['alunos'] = selecao_de_alunos

    return render(request, template_name='graphs.html', context=context, status=200)