from django.shortcuts import render
from .mock import data

def home(request):
    context = {
        'data': data,
    }
    return render(request, 'home.html', context)