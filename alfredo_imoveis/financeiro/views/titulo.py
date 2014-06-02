# encoding: utf8
__author__ = 'gpzim98'
from django.shortcuts import render, get_object_or_404
from financeiro.models.titulo import Titulo, Recibo
from funcionarios.models import Funcionario
from financeiro.forms.titulo import TituloForm
from parametros.models import ParametrosGerais
from datetime import datetime, date
from decimal import *


today = date.today()

template_home = 'financeiro/titulo/home.html'
template_novo = 'financeiro/titulo/novo.html'
template_detalhe = 'financeiro/titulo/detalhe.html'
template_relatorio = 'financeiro/titulo/relatorio.html'
template_recibo = 'financeiro/titulo/recibo.html'
template_carta_cobranca_modelo_1 = 'financeiro/titulo/carta_cobranca_modelo_1.html'
template_carta_cobranca_modelo_2 = 'financeiro/titulo/carta_cobranca_modelo_2.html'
template_carta_cobranca_modelo_3 = 'financeiro/titulo/carta_cobranca_modelo_3.html'

def home(request):
    dados = {}
    funcionario = Funcionario.objects.filter(usuario=request.user)
    dados['titulos'] = Titulo.objects.filter(empresa=funcionario[0].empresa, deletado=False)
    return render(request, template_home, dados)

def detalhe(request,id,mensagem=''):
    dados = {}
    dados['mensagem'] = mensagem
    titulo = get_object_or_404(Titulo, id=id)
    dados['form'] = TituloForm(instance=titulo)
    dados['titulo'] = titulo
    recibos = Recibo.objects.filter(titulo=titulo)
    dados['recibos'] = recibos
    dados['multa'] = titulo.multa
    dados['juros'] = titulo.juros
    informacoes_titulo(dados,titulo)
    return render(request, template_detalhe, dados)

def delete(request, id):
    titulo = Titulo.objects.get(id=id)
    titulo.deletado = True
    titulo.save()
    return home(request)

def filtrar(request):
    dados = {}

    if request.POST['dataini'] and request.POST['datafim']:
        dataini = datetime.strptime(request.POST['dataini'], '%Y-%m-%d')
        datafim = datetime.strptime(request.POST['datafim'], '%Y-%m-%d')
    else:
        dataini = datetime.strptime('1900-01-01', '%Y-%m-%d')
        datafim = datetime.strptime('2500-12-31', '%Y-%m-%d')

    if request.POST.get('valor_titulo', False):
        valorini=float(request.POST.get('valor_titulo', False))
        valorfim=float(request.POST.get('valor_titulo', False))
    else:
        valorini=0
        valorfim=999999

    if request.POST['tipo'] in ('R', 'D'):
        tipo = request.POST['tipo']
    else:
        tipo = ''

    dados['titulos'] = Titulo.objects.filter(empresa__nome__contains=request.POST['empresa'],
                                             deletado=request.POST.get('deletados', False),
                                             descricao__contains=request.POST['descricao'],
                                             conta_caixa__descricao__contains=request.POST['conta_caixa'],
                                             vencimento__range=[dataini, datafim],
                                             valor__range=[valorini, valorfim],
                                             tipo__contains=tipo)

    if request.POST.get('relatorio', False):
        dados['data'] = today
        return render(request,template_relatorio,dados)
    else:
        return render(request, template_home,dados)

def salvar(request,id):
    dados = {}
    form = TituloForm(request.POST or None)

    if form.is_valid():
        titulo = form.save(commit=False)

        if id not in (None, '0'):
            titulo.id = id

        titulo.usuario_cadastrou = request.user
        titulo.data_cadastro = today
        titulo.save()
        mensagem = 'Título salvo com sucesso!'
        return detalhe(request, titulo.id, mensagem)
    else:
        dados['form'] = form
        dados['erros'] = form.errors
        return render(request, template_novo, dados)

def adicionar(request):
    dados = {}
    dados['form'] = TituloForm()
    return render(request, template_novo, dados)

def recibo(request,id):
    dados = {}
    titulo = get_object_or_404(Titulo,pk=id)
    recibo = Recibo(titulo=titulo, data_cadastro=today,usuario=request.user,descricao='...')
    recibo.save()
    dados['recibo'] = recibo
    return render(request, template_recibo, dados)

def carta_cobranca_modelo_1(request,id):
    dados = {}
    dados['data'] = today
    dados['titulo'] = get_object_or_404(Titulo,pk=id)
    return render(request, template_carta_cobranca_modelo_1,dados)

def carta_cobranca_modelo_2(request,id):
    dados = {}
    dados['data'] = today
    titulo = get_object_or_404(Titulo,pk=id)
    dados['titulo'] = titulo
    data_de = date(titulo.vencimento.year, titulo.vencimento.month+1,titulo.vencimento.day)
    dados['periodo_de'] = titulo.vencimento
    dados['periodo_ate'] = data_de
    return render(request, template_carta_cobranca_modelo_2,dados)

def carta_cobranca_modelo_3(request,id):
    dados = {}
    dados['data'] = today
    dados['titulo'] = get_object_or_404(Titulo,pk=id)
    return render(request, template_carta_cobranca_modelo_3,dados)    

def abater_titulo(request,id):
    dados = {}
    
    titulo = get_object_or_404(Titulo, pk=id)
    #import pdb;pdb.set_trace()

    titulo.multa = titulo.multa + Decimal(request.POST.get('multa',0))
    titulo.juros = titulo.juros + Decimal(request.POST.get('juros',0))
    titulo.pagamento_parcial = titulo.pagamento_parcial + Decimal(request.POST.get('valor',0))
    titulo.save()

    return detalhe(request,id)

def informacoes_titulo(dados = {}, titulo=None):
    parametros = get_object_or_404(ParametrosGerais, pk=1)

    # Calculando a multa restante
    dados['multa_restante'] = 0

    if (titulo.vencimento < today) and (titulo.valor > titulo.pagamento_parcial):
        dados['atrasado'] = 'Sim'
        if (parametros.multa - titulo.multa) > 0:
            dados['multa_restante'] = (parametros.multa - titulo.multa)

    dados['juros_restantes'] = 0            
    
    # Calculando o valor restante e o juros restante
    if (titulo.valor - titulo.pagamento_parcial) > 0:
        dados['valor_restante'] = titulo.valor - titulo.pagamento_parcial
        if titulo.vencimento < today:
            dados['juros_restantes'] = ((titulo.valor - titulo.pagamento_parcial)  * parametros.taxa_juros)/100
    else:
        dados['valor_restante'] = 0


