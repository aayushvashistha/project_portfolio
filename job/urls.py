from django.urls import path
from job import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('work', views.work, name='work'),
    path("work/<int:pk>", views.detail, name="detail"),
    path('about', views.about, name='about'),
]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)