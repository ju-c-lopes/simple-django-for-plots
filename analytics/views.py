from django.shortcuts import render, redirect
from django.contrib import messages
from analytics.models import Aluno, Prova, possiveis_notas
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io, base64

# Create your views here.

def consultar_aluno(request):
    context = None
    aluno = None
    if request.GET:
        print(request.GET)
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
    print(request.POST)
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
        print(request.POST)
        print("PRINT REQUEST TODOS", request.POST.get("todos", "não retornou"))
        
        alunos = request.POST.getlist("alunos")
        if 'all' in alunos:
            selecao_de_alunos = Aluno.objects.all()
        else:
            todos_alunos = Aluno.objects.all()
            for i in range(len(todos_alunos)):
                for id_aluno in alunos:
                    if todos_alunos[i].id == id_aluno:
                        selecao_de_alunos.append(todos_alunos[i])

        notas = []
        for aluno in selecao_de_alunos:
            print("ALUNO NOTA FIRST: ", aluno.notas.first().nota)
            notas.append(aluno.notas.first())
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(
            [aluno.nome for aluno in selecao_de_alunos],
            [nota.nota for nota in notas],
            '--bo')
        ax.set_title('Notas de alunos')
        ax.set_xlabel('Alunos')
        ax.set_ylabel('Notas')
        
        file_io = io.BytesIO()
        fig.savefig(file_io)
        b64 = base64.b64encode(file_io.getvalue()).decode()
        context['chart'] = b64
        print("INSTANCIADO CHART")
        #print(context['chart'])

    context['alunos'] = selecao_de_alunos

    print('chart' in context.keys())

    return render(request, template_name='graphs.html', context=context, status=200)