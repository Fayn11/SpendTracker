from django.shortcuts import render


def start(request):
    return render(request, 'aplicatie1/start.html')
