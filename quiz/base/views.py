from django.http import HttpResponse
from django.shortcuts import render


def home(requisicao):
    return HttpResponse('ola MUndo')

