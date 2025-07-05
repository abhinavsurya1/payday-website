from django import forms
from django.utils import timezone
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'requirements', 'job_type', 'location', 'salary_range', 'deadline', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Describe the job responsibilities and requirements...'}),
            'requirements': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'List the key requirements and qualifications...'}),
            'deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter job title'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter job location'}),
            'salary_range': forms.Select(choices=Job.SALARY_RANGE_CHOICES, attrs={'class': 'form-control'}),
            'job_type': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        if deadline and deadline < timezone.now().date():
            raise forms.ValidationError("Deadline cannot be in the past.")
        return deadline

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Job title must be at least 5 characters long.")
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 50:
            raise forms.ValidationError("Job description must be at least 50 characters long.")
        return description

    def clean_requirements(self):
        requirements = self.cleaned_data.get('requirements')
        if len(requirements) < 30:
            raise forms.ValidationError("Job requirements must be at least 30 characters long.")
        return requirements 