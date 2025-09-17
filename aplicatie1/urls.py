from django.contrib.auth.views import LoginView
from django.urls import path, include
from aplicatie1 import views
from django.conf.urls.static import static
from django.conf import settings


app_name = 'start'

urlpatterns = [
    path('', views.start, name='start'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
