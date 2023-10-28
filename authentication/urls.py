from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.authentication, name="auth_login"),
    path('logout/', views.sign_out, name="auth_logout"),
]
