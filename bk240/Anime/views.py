from django.shortcuts import render

from Form.Index import Index


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
