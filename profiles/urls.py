from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('candidate/register/', views.candidate_register, name='candidate_register'),
    path('client/register/', views.client_register, name='client_register'),
    path('candidate/profile/', views.candidate_profile, name='candidate_profile'),
    path('client/profile/', views.client_profile, name='client_profile'),
    path('client/upload-document/', views.upload_verification_document, name='upload_verification_document'),
    path('candidate/dashboard/', views.candidate_dashboard, name='candidate_dashboard'),
    path('client/dashboard/', views.client_dashboard, name='client_dashboard'),
    path('candidate/bank-details/', views.bank_details_view, name='bank_details'),
    path('candidate/id-verification/', views.id_verification_view, name='id_verification'),
] 