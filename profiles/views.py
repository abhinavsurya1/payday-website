from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import CandidateProfile, ClientProfile, VerificationDocument, UserRegistrationType, BankDetails
from .forms import CandidateRegistrationForm, ClientRegistrationForm, CandidateProfileForm, ClientProfileForm, BankDetailsForm
from jobs.models import Job, JobApplication
from .utils import notify_profile_update, notify_verification_status
import os
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def candidate_register(request):
    if request.method == 'POST':
        form = CandidateRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                # Set registration type
                UserRegistrationType.objects.create(user=user, type='candidate')
                login(request, user)
                messages.success(request, 'Registration successful! Please complete your profile.')
                return redirect('profiles:candidate_profile')
            except Exception as e:
                messages.error(request, 'An error occurred during registration. Please try again.')
                print(f"Registration error: {str(e)}")
    else:
        form = CandidateRegistrationForm()
    return render(request, 'profiles/candidate_register.html', {'form': form})

def client_register(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                # Set registration type
                UserRegistrationType.objects.create(user=user, type='client')
                # Create an empty client profile
                ClientProfile.objects.create(
                    user=user,
                    company_name='',  # These will be filled out later
                    industry='OTHER',
                    gst_number='PENDING',  # Temporary value
                    company_address='',
                    phone_number='',
                    preferred_candidate_requirements=''
                )
                
                # Send welcome notifications
                notify_profile_update(user, 'client')
                
                messages.success(request, 'Registration successful! Please complete your company profile.')
                login(request, user)  # Log the user in
                return redirect('profiles:client_profile')  # Redirect to profile completion
            except Exception as e:
                messages.error(request, 'An error occurred during registration. Please try again.')
                print(f"Registration error: {str(e)}")
    else:
        form = ClientRegistrationForm()
    return render(request, 'profiles/client_register.html', {'form': form})

@login_required
def candidate_profile(request):
    try:
        profile = request.user.candidate_profile
    except CandidateProfile.DoesNotExist:
        profile = None
    
    if request.method == 'POST':
        form = CandidateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            
            # Send profile update notifications
            notify_profile_update(request.user, 'candidate')
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('profiles:candidate_dashboard')
    else:
        form = CandidateProfileForm(instance=profile)
    
    return render(request, 'profiles/candidate_profile.html', {
        'form': form,
        'profile': profile
    })

@login_required
def client_profile(request):
    try:
        profile = request.user.client_profile
    except ClientProfile.DoesNotExist:
        profile = None
    
    if request.method == 'POST':
        form = ClientProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            
            # Send profile update notifications
            notify_profile_update(request.user, 'client')
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('profiles:client_profile')
    else:
        form = ClientProfileForm(instance=profile)
    
    return render(request, 'profiles/client_profile.html', {
        'form': form,
        'profile': profile
    })

@login_required
def upload_verification_document(request):
    if not hasattr(request.user, 'client_profile'):
        messages.error(request, 'Only clients can upload verification documents.')
        return redirect('home')
    
    profile = request.user.client_profile
    
    if request.method == 'POST':
        document_type = request.POST.get('document_type')
        document = request.FILES.get('document')
        
        if document and document_type:
            VerificationDocument.objects.create(
                client=profile,
                document_type=document_type,
                document=document
            )
            messages.success(request, 'Verification document uploaded successfully!')
            
            # Check if all required documents are uploaded
            required_docs = ['GST', 'PAN']
            uploaded_docs = set(profile.verification_documents.values_list('document_type', flat=True))
            
            if all(doc in uploaded_docs for doc in required_docs):
                profile.is_verified = True
                profile.save()
                notify_verification_status(request.user, 'client', True)
            else:
                notify_verification_status(request.user, 'client', False)
                
            return redirect('profiles:client_profile')
        else:
            messages.error(request, 'Please provide both document type and file.')
    
    return render(request, 'profiles/upload_verification_document.html', {
        'profile': profile
    })

@login_required
def candidate_dashboard(request):
    if not hasattr(request.user, 'candidate_profile'):
        messages.error(request, 'Access denied. Candidate profile required.')
        return redirect('home')
    
    profile = request.user.candidate_profile
    job_applications = JobApplication.objects.filter(candidate=request.user).order_by('-applied_at')
    
    context = {
        'profile': profile,
        'job_applications': job_applications,
        'total_applications': job_applications.count(),
        'pending_applications': job_applications.filter(status='PENDING').count(),
        'shortlisted_applications': job_applications.filter(status='SHORTLISTED').count(),
    }
    return render(request, 'profiles/candidate_dashboard.html', context)

@login_required
def client_dashboard(request):
    if not hasattr(request.user, 'client_profile'):
        messages.error(request, 'Access denied. Client profile required.')
        return redirect('home')
    
    profile = request.user.client_profile
    posted_jobs = Job.objects.filter(client=request.user).order_by('-created_at')
    total_applications = JobApplication.objects.filter(job__client=request.user).count()
    shortlisted_candidates = JobApplication.objects.filter(job__client=request.user, status='SHORTLISTED').count()
    
    context = {
        'profile': profile,
        'posted_jobs': posted_jobs,
        'total_applications': total_applications,
        'shortlisted_candidates': shortlisted_candidates,
        'active_jobs': posted_jobs.filter(is_active=True).count(),
    }
    return render(request, 'profiles/client_dashboard.html', context)

@login_required
def id_verification_view(request):
    # Check if the user is a candidate
    if not hasattr(request.user, 'candidate_profile') or request.user.candidate_profile is None:
        messages.error(request, "You must be a candidate to access this page.")
        return redirect('home') # Redirect to home or another appropriate page

    # Placeholder logic for ID verification
    if request.method == 'POST':
        # In a real implementation, you would handle file uploads, send to Persona, etc.
        messages.info(request, "ID verification process would be initiated here.")
        return redirect('profiles:candidate_dashboard') # Redirect after initiation

    context = {
        'id_types': ['Voter ID', 'PAN Card', 'Aadhaar Card', 'Passport'], # Updated ID types
        'is_authenticated': request.user.is_authenticated, # For navbar visibility
        'profile_type': 'candidate' # For navbar visibility
    }
    return render(request, 'profiles/id_verification.html', context)

@login_required
def bank_details_view(request):
    # Check if the user is a candidate
    if not hasattr(request.user, 'candidate_profile') or request.user.candidate_profile is None:
        messages.error(request, "You must be a candidate to access this page.")
        return redirect('home') # Redirect to home or another appropriate page

    candidate_profile = request.user.candidate_profile

    try:
        # Try to get existing bank details
        bank_details_instance = candidate_profile.bank_details
    except BankDetails.DoesNotExist:
        # Create a new instance if it doesn't exist
        bank_details_instance = BankDetails(candidate_profile=candidate_profile)

    if request.method == 'POST':
        form = BankDetailsForm(request.POST, instance=bank_details_instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Your bank details have been saved.")
            return redirect('profiles:candidate_dashboard') # Redirect to candidate dashboard or similar
    else:
        form = BankDetailsForm(instance=bank_details_instance)

    context = {
        'form': form,
        'is_authenticated': request.user.is_authenticated, # Include this for navbar visibility check
        'profile_type': 'candidate' # Indicate profile type for navbar
    }
    return render(request, 'profiles/bank_details_form.html', context)
