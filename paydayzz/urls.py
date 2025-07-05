"""
URL configuration for paydayzz project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include, reverse
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.shortcuts import redirect
from . import views

def logout_view(request):
    logout(request)
    return redirect('home')

class CustomLoginView(auth_views.LoginView):
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
            
        user = self.request.user
        if hasattr(user, 'candidate_profile'):
            return reverse('profiles:candidate_dashboard')
        elif hasattr(user, 'client_profile'):
            return reverse('profiles:client_dashboard')
        return reverse('home')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('jobs/', include('jobs.urls')),
    path('profiles/', include('profiles.urls')),
    # Authentication URLs
    path('login/', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
