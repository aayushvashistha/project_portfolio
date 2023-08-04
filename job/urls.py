from django.urls import path
from job import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('work', views.index, name='index'),
    path('', views.home, name='home'),
    path("<int:pk>/", views.detail, name="detail"),
]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)