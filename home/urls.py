from django.urls import path
from home import views

urlpatterns = [ 
    path("",views.home, name='home'),
    path("internship/",views.internship, name='internship'),
    path("about/",views.about, name='about'),
    path("services/",views.services, name='services'),
    path("contact/",views.contact, name='contact'),
]
