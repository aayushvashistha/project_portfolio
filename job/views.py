from django.shortcuts import render
from job.models import Project
# from rest_framework import generics

# Create your views here.

def work(request):
    projects = Project.objects.all()
    context = {
        'projects': projects
    }
    return render(request, 'work.html', context)

def detail(request, pk):
    project = Project.objects.get(pk=pk)
    context = {
        'project': project
    }
    return render(request, 'detail.html', context)

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')