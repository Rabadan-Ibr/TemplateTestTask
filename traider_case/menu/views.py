from django.shortcuts import render


def index(request):
    text = request.path
    return render(request, 'index.html', {'text': text})


def not_found(request):
    return render(request, '404.html')
