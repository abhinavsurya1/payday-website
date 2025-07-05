from django.shortcuts import render, HttpResponse
from jobs.models import Job

'''def home(request):
    """Redirects users to the login page if not authenticated, else to the dashboard."""
    if request.user.is_authenticated:
        return redirect("dashboard")  # Redirect to the dashboard if logged in
    return redirect("/accounts/login/")  # Redirect to login page

@login_required
def dashboard(request):
    """Displays the user dashboard after login."""
    return render(request, "dashboard.html")  # Ensure dashboard.html exists in users/templates/
'''

##
def home(request):
    latest_jobs = Job.objects.filter(is_active=True).order_by('-created_at')[:6]
    context = {
        'latest_jobs': latest_jobs,
    }
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'home/about.html')

def internship(request):
    return render(request, 'home/internship.html')

def services(request):
    return render(request, 'home/services.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        
        # For now, just display the submitted data
        return HttpResponse(f"Thank you {name}, we received your message!")

    return render(request, "home/contact.html")