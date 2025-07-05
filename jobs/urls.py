from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('<int:pk>/', views.job_detail, name='job_detail'),
    path('post/', views.post_job, name='post_job'),
    path('manage/', views.manage_jobs, name='manage_jobs'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('<int:pk>/edit/', views.job_edit, name='job_edit'),
    path('<int:pk>/delete/', views.job_delete, name='job_delete'),
    path('<int:pk>/apply/', views.job_apply, name='job_apply'),
    path('post-job-ajax/', views.post_job_ajax, name='post_job_ajax'),
    path('post-success/', views.job_post_success, name='job_post_success'),
    path('<int:job_id>/applications/', views.review_applications, name='review_applications'),
    path('application/<int:app_id>/status/', views.update_application_status, name='update_application_status'),
] 