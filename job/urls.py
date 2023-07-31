from django.urls import path
from job import views

urlpatterns = [
    path('', views.index, name='index'),
    path("<int:pk>/", views.detail, name="detail"),
]