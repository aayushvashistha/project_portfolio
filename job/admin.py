from django.contrib import admin
from .models import Project, Resume
# Register your models here.

admin.site.register({Project, Resume})