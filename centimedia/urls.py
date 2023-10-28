"""
URL configuration for centimedia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render, redirect, reverse

from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse


def main_dashboard(request):
    if request.user.is_authenticated:
        return render(request, "pages/dashboard.html")
    else:
        return redirect(reverse("auth_login"))


urlpatterns = [
                  path('auth/', include("authentication.urls")),
                  path('centimedia/', include("media_manager.urls")),
                  path('centimedia/', include("organisations.urls")),
                  path('admin/', admin.site.urls),
                  path('centimedia', main_dashboard, name="dashboard"),
                  path('', include("portal.urls"))
              ] \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
