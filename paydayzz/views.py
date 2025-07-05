from django.shortcuts import render, redirect
from django.contrib import messages

def home(request):
    context = {
        'is_authenticated': request.user.is_authenticated
    }
    
    if request.user.is_authenticated:
        # First, determine if the user registered as a client or candidate
        registration_type = None
        
        # Check if user has a client profile
        if hasattr(request.user, 'client_profile'):
            if request.user.client_profile is not None:
                registration_type = 'client'
                context['profile_type'] = 'client'
                context['profile'] = request.user.client_profile
        # Check if user has a candidate profile
        elif hasattr(request.user, 'candidate_profile'):
            if request.user.candidate_profile is not None:
                registration_type = 'candidate'
                context['profile_type'] = 'candidate'
                context['profile'] = request.user.candidate_profile
        
        # If no profile exists yet, check registration type
        if not registration_type:
            if hasattr(request.user, 'registration_type'):
                registration_type = request.user.registration_type.type
            else:
                # Default to candidate if no registration type is set (fallback)
                registration_type = 'candidate'
        
        context['registration_type'] = registration_type
    
    return render(request, 'home.html', context)

def contact(request):
    return render(request, 'contact.html') 