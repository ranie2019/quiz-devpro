from django.shortcuts import render, redirect
from quiz.base.forms import AlunoForm
from quiz.base.models import Pergunta, Aluno


def home(requisicao):
    if requisicao.method == 'POST':
        # Usuario ja Existe
        email = requisicao.POST['email']
        try:
            aluno = Aluno.objects.get(email=email)
        except Aluno.DoesNotExist:
            # Usuario nao Existe
            formulario = AlunoForm(requisicao.POST)
            if formulario.is_valid():
                aluno = formulario.save()
                requisicao.session['aluno_id'] = aluno.id
                return redirect('/perguntas/1')
            else:
                contexto = {'formulario': formulario}
                return render(requisicao, 'base/home.html', contexto)
        else:
            requisicao.session['aluno_id'] = aluno.id
    return render(requisicao, 'base/home.html')


def classificacao(requisicao):
    return render(requisicao, 'base/classificacao.html')


def perguntas(requisicao, indice):
    try:
        aluno_id = requisicao.session['aluno_id']
    except KeyError:
        return redirect('/')
    else:
        try:
            pergunta = Pergunta.objects.filter(disponivel=True).order_by('id')[indice - 1]
        except IndexError:
            return redirect('/classificacao')
        else:
            contexto = {'indice_da_questao': indice, 'pergunta': pergunta}
            if requisicao.method == 'POST':
                resposta_indice = int(requisicao.POST['resposta_indice'])
                if resposta_indice == pergunta.alternativas_correta:
                    # Amazenar dados da resposta
                    return redirect(f'perguntas/{indice + 1}')
                contexto['resposta_indice'] = resposta_indice
            return render(requisicao, 'base/game.html', context=contexto)

