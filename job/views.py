from django.shortcuts import render
from job.models import Project, Resume
from django.http import FileResponse, StreamingHttpResponse
from django.conf import settings
import os

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

def download(request):
    # cv_file_path = os.path.join(settings.MEDIA_ROOT, 'documents/Aayush_Vashistha_CV.pdf')
    # print(cv_file_path)

    # # Open the file and serve it using FileResponse
    # with open(cv_file_path, 'rb') as pdf_file:
    #     print("inside open file-------------------------------", pdf_file)
    #     response = StreamingHttpResponse(pdf_file, content_type='application/pdf')
    #     print("-------------------1st-----------------", response)
    #     response['Content-Disposition'] = 'attachment; filename="Aayush_Vashistha_CV.pdf"'
    #     print("-------------------2nd-----------------", response)
    #     # pdf_file.close()
    #     return response

    cv_file_path = os.path.join(settings.MEDIA_ROOT, 'documents/Aayush_Vashistha_CV.pdf')
    print(cv_file_path)

    def file_iterator(file_path, chunk_size=8192):
        with open(file_path, 'rb') as pdf_file:
            while True:
                chunk = pdf_file.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    response = StreamingHttpResponse(file_iterator(cv_file_path), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Aayush_Vashistha_CV.pdf"'
    return response
    
# /Users/aayush/Downloads/git/project_portfolio/documents/Aayush_Vashistha_CV.pdf