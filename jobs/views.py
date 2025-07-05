from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Job, JobApplication
from .forms import JobForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .utils import send_shortlisted_notification

def job_list(request):
    # Get filter parameters
    job_type = request.GET.get('job_type')
    location = request.GET.get('location')
    salary_range = request.GET.get('salary_range')
    search = request.GET.get('search')
    
    # Start with all active jobs
    jobs = Job.objects.filter(is_active=True)
    
    # Apply filters
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    if location:
        jobs = jobs.filter(location__icontains=location)
    if salary_range:
        jobs = jobs.filter(salary_range=salary_range)
    if search:
        jobs = jobs.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(requirements__icontains=search)
        )
    
    # Order by creation date
    jobs = jobs.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(jobs, 9)  # Show 9 jobs per page
    page_number = request.GET.get('page')
    jobs = paginator.get_page(page_number)
    
    # Get job types for filter dropdown
    job_types = Job.JOB_TYPE_CHOICES
    
    context = {
        'jobs': jobs,
        'job_types': job_types,
    }
    return render(request, 'jobs/job_list.html', context)

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk, is_active=True)
    
    # Check if user has already applied
    has_applied = False
    if request.user.is_authenticated and hasattr(request.user, 'candidate_profile'):
        has_applied = JobApplication.objects.filter(job=job, candidate=request.user).exists()
    
    context = {
        'job': job,
        'has_applied': has_applied,
    }
    return render(request, 'jobs/job_detail.html', context)

@login_required
def post_job(request):
    if not hasattr(request.user, 'client_profile'):
        messages.error(request, 'Only clients can post jobs.')
        return redirect('home')
    profile = request.user.client_profile
    is_verified = profile.is_verified

    if request.method == 'POST':
        form = JobForm(request.POST)
        if is_verified and form.is_valid():
            job = form.save(commit=False)
            job.client = request.user
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('jobs:manage_jobs')
        elif not is_verified:
            messages.error(request, 'You must verify your company profile before posting jobs.')
        else:
            print('JobForm errors:', form.errors)
            messages.error(request, 'Please correct the errors below.')
    else:
        form = JobForm()

    return render(request, 'jobs/post_job.html', {'form': form, 'is_verified': is_verified})

@login_required
def manage_jobs(request):
    if not hasattr(request.user, 'client_profile'):
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    jobs = Job.objects.filter(client=request.user).order_by('-created_at')
    return render(request, 'jobs/manage_jobs.html', {'jobs': jobs})

@login_required
def my_applications(request):
    if not hasattr(request.user, 'candidate_profile'):
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    applications = JobApplication.objects.filter(candidate=request.user).order_by('-applied_at')
    return render(request, 'jobs/my_applications.html', {'applications': applications})

@login_required
def job_edit(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if job.client != request.user:
        messages.error(request, 'You do not have permission to edit this job.')
        return redirect('jobs:job_detail', pk=pk)
    
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('jobs:job_detail', pk=pk)
    else:
        form = JobForm(instance=job)
    
    return render(request, 'jobs/job_edit.html', {'form': form, 'job': job})

@login_required
def job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if job.client != request.user:
        messages.error(request, 'You do not have permission to delete this job.')
        return redirect('jobs:job_detail', pk=pk)
    
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully!')
        return redirect('jobs:manage_jobs')
    
    return render(request, 'jobs/job_confirm_delete.html', {'job': job})

@login_required
def job_apply(request, pk):
    if not hasattr(request.user, 'candidate_profile'):
        messages.error(request, 'Only candidates can apply for jobs.')
        return redirect('jobs:job_detail', pk=pk)
    
    job = get_object_or_404(Job, pk=pk)
    if JobApplication.objects.filter(job=job, candidate=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('jobs:job_detail', pk=pk)
    
    if request.method == 'POST':
        cover_letter = request.POST.get('cover_letter', '').strip()
        JobApplication.objects.create(
            job=job,
            candidate=request.user,
            status='PENDING',
            cover_letter=cover_letter
        )
        messages.success(request, 'Application submitted successfully!')
        return redirect('jobs:my_applications')
    else:
        return redirect('jobs:job_detail', pk=pk)

@login_required
@csrf_exempt
def post_job_ajax(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = JobForm(request.POST)
        profile = request.user.client_profile
        if not profile.is_verified:
            return JsonResponse({'success': False, 'error': 'Profile not verified.'}, status=400)
        if form.is_valid():
            job = form.save(commit=False)
            job.client = request.user
            job.save()
            return JsonResponse({
                'success': True,
                'job': {
                    'id': job.id,
                    'title': job.title,
                    'location': job.location,
                    'salary_range': job.salary_range,
                    'description': job.description,
                    'requirements': job.requirements,
                    'deadline': job.deadline.strftime('%Y-%m-%d') if job.deadline else '',
                }
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

def job_post_success(request):
    return render(request, 'jobs/job_post_success.html')

@login_required
def review_applications(request, job_id):
    job = get_object_or_404(Job, pk=job_id, client=request.user)
    applications = job.jobapplication_set.all()
    return render(request, 'jobs/review_applications.html', {'job': job, 'applications': applications})

@login_required
@require_POST
def update_application_status(request, app_id):
    application = get_object_or_404(JobApplication, pk=app_id, job__client=request.user)
    status = request.POST.get('status')
    if status in ['SHORTLISTED', 'REJECTED', 'HIRED']:
        application.status = status
        application.save()
        
        # Send email notification if shortlisted
        if status == 'SHORTLISTED':
            send_shortlisted_notification(application)
        
        return JsonResponse({'success': True, 'new_status': status})
    return JsonResponse({'success': False, 'error': 'Invalid status'}, status=400)
