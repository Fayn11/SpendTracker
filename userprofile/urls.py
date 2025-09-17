from django.urls import path
from userprofile import views

app_name = 'userprofile'

urlpatterns = [
    path('new_account/', views.CreateNewAccount.as_view(), name='utilizator_nou'),
    path('register_success/', views.register_success, name='inregistrare_reusita'),
]
