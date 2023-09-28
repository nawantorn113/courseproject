from django.shortcuts import render
from . import models
# Create your views here.

def index(request):
    context = {}
    context['subjects'] = models.Classes.objects.all()
    return render(request, 'index.html', context)


def category(request, id):
    context = {}
    context['subjects'] = models.Classes.objects.filter(class_category=id)

    return render(request, 'category.html', context)