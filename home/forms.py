'''from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomSignupForm(forms.Form):  # Don't inherit from SignupForm
    role = forms.ChoiceField(
        choices=[('candidate', 'Candidate'), ('client', 'Client')],
        required=True
    )

    def save(self, request, user=None):
        if not user:
            user = User.objects.create()  # Ensure user exists
        user.role = self.cleaned_data['role']
        user.save()
        return user

    def signup(self, request, user):  # Required for Allauth
        user.role = self.cleaned_data.get('role', 'candidate')  # Default role
        user.save()
        return user'''
