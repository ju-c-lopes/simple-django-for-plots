from django.shortcuts import render, redirect
from django.contrib import messages
from analytics.models import Aluno, Prova, possiveis_notas

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
                for aluno in alunos:
                    if todos_alunos[i].id == aluno:
                        selecao_de_alunos.append(todos_alunos[i])
    context = {
        'alunos': selecao_de_alunos,
    }

    return render(request, template_name='graphs.html', context=context, status=200)