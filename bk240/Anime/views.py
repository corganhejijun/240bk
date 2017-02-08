from django.shortcuts import render

from Form.Index import Index
from Form.Ftp import Ftp


def index(request):
    if request.method == 'GET':
        form = Index()
        return form.get(request)
    if request.method == 'POST':
        form = Index(request.POST)
        return form.post(request)


def aidPage(request, aid):
    if request.method == 'GET':
        return render(request, 'html/' + aid + '.html')


def ftp(request):
    if request.method == 'GET':
        form = Ftp()
        return form.get(request)
    if request.method == 'POST':
        form = Ftp()
        return form.post(request)
