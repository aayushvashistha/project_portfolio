from django.shortcuts import render, HttpResponse
from job.models import Project
from django.http import StreamingHttpResponse
from django.conf import settings
import time
import os, sys, subprocess, re, ast

streamlit_app_path = os.path.join(os.path.dirname(__file__), "Project1.py")

def run_streamlit_app(app_path):
    command = f"streamlit run {app_path}"
    process = subprocess.Popen(command, shell=True)
    return process

# Create your views here.
def work(request):
    projects = Project.objects.all()
    context = {
        'projects': projects
    }
    return render(request, 'work.html', context)

def detail(request, pk):
    project = Project.objects.get(pk=pk)
    print(project, pk)
    context = {
        'project': project
    }

    if pk == 1:
        run_streamlit_app(streamlit_app_path)
        time.sleep(5)
    
    return render(request, 'detail.html', context)
    

def home(request):
    try:
        # Path to the external script
        script_path = os.path.join(os.path.dirname(__file__), 'stocks.py')

        # Run the external script and capture the output
        result = subprocess.run(['python', script_path], capture_output=True, text=True)
        match = re.search(r'{.*}',result.stdout)
        if match:
            dict_str = match.group(0)
            result_dict = ast.literal_eval(dict_str)
            print(result_dict)
        else:
            print("No dictionary found in the string.")

    except Exception as e:
        # Handle exceptions, if any
        result_dict = f"Error: Stock data currently not available, try reloading the page{str(e)}"

    return render(request, 'home.html', {'result_dict': result_dict})

def about(request):
    return render(request, 'about.html')

def download(request):
    cv_file_path = os.path.join(settings.MEDIA_ROOT, 'documents\Aayush_Vashistha_backend.pdf')
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