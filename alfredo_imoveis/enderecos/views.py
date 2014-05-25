# encoding: utf-8
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages

from forms import BairroForm
from models import Bairro, Cidade

# Create your views here.
template_bairro_novo = 'enderecos/bairro/bairro.html'
template_bairro_add = 'enderecos/bairro/bairro_add.html'

mensagem_geral = 'Aloow'

def bairro_home(request,dados={}):
    dados['lista_bairros'] = Bairro.objects.all().order_by('id')
    form = BairroForm()
    dados['form'] = form
    return render(request,template_bairro_novo,dados)

def bairro_detalhe(request, id):
    dados = {}
    bairro = get_object_or_404(Bairro, id=id)
    form = BairroForm(instance=bairro)
    dados['lista_bairros'] = Bairro.objects.all()
    dados['form'] = form
    dados['bairro'] = bairro
    dados['detalhe'] = 'detalhe'
    return render(request,template_bairro_add,dados)

def bairro_adiciona(request):
    dados = {}
    form = BairroForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            bairro = form.save()
            dados['mensagem'] = 'Bairro {nome} cadastrado com sucesso'.format(nome=bairro.nome)
            return bairro_home(request,dados)
        else:
            dados['form'] = form
            return render(request, template_bairro_add, dados)
    else:
        dados['form'] = form
        return render(request, template_bairro_add, dados)

def bairro_update(request, id):
    form = BairroForm(request.POST or None)
    if form.is_valid():
        bairro = form.save(commit=False)
        bairro.id = id
        bairro.save()
        return bairro_home(request)
    else:
        dados = {}
        dados['form'] = form

class BairroDelete(DeleteView):
    model = Bairro
    success_url = reverse_lazy('app_enderecos_bairro_home')
    template_name = 'enderecos/bairro/bairro_confirm_delete.html'    

# Views de cidade
class CidadeList(ListView):
    template_name = 'enderecos/cidade/cidade_list.html'
    model = Cidade

class CidadeCreate(CreateView):
    model = Cidade
    template_name = 'enderecos/cidade/cidade_form.html'
    success_url = reverse_lazy('app_enderecos_cidade_home')
    success_message = "was created successfully"

class CidadeUpdate(UpdateView):
    model = Cidade
    success_url = reverse_lazy('app_enderecos_cidade_home')
    template_name = 'enderecos/cidade/cidade_form.html'

class CidadeDelete(DeleteView):
    model = Cidade
    success_url = reverse_lazy('app_enderecos_cidade_home')
    template_name = 'enderecos/cidade/cidade_confirm_delete.html'    