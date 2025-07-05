from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CandidateProfile, ClientProfile, BankDetails

class CandidateRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class ClientRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = [
            'phone_number', 'whatsapp_number', 'date_of_birth', 'address',
            'preferred_job_type', 'skills', 'experience',
            'cv', 'profile_picture', 'additional_pictures', 'photo_id'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'skills': forms.Textarea(attrs={'rows': 3}),
            'experience': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field in self.fields.values():
            if isinstance(field, forms.TextInput):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field, forms.Textarea):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            elif isinstance(field, forms.FileInput):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field, forms.DateInput):
                field.widget.attrs.update({'class': 'form-control'})

    def clean_cv(self):
        cv = self.cleaned_data.get('cv')
        if cv:
            if cv.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError('CV file size must not exceed 5MB')
            if not cv.name.lower().endswith(('.pdf', '.doc', '.docx')):
                raise forms.ValidationError('CV must be a PDF or Word document')
        return cv

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            if picture.size > 2 * 1024 * 1024:  # 2MB limit
                raise forms.ValidationError('Profile picture size must not exceed 2MB')
            if not picture.content_type.startswith('image/'):
                raise forms.ValidationError('Profile picture must be an image file')
        return picture

    def clean_photo_id(self):
        photo_id = self.cleaned_data.get('photo_id')
        if photo_id:
            if photo_id.size > 2 * 1024 * 1024:  # 2MB limit
                raise forms.ValidationError('Photo ID size must not exceed 2MB')
            if not photo_id.content_type.startswith('image/'):
                raise forms.ValidationError('Photo ID must be an image file')
        return photo_id

    def clean_additional_pictures(self):
        pictures = self.cleaned_data.get('additional_pictures')
        if pictures:
            if pictures.size > 2 * 1024 * 1024:  # 2MB limit
                raise forms.ValidationError('Additional picture size must not exceed 2MB')
            if not pictures.content_type.startswith('image/'):
                raise forms.ValidationError('Additional picture must be an image file')
        return pictures

class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = [
            'company_name', 'industry', 'gst_number', 'company_address',
            'phone_number', 'whatsapp_number', 'company_website', 'company_logo',
            'preferred_candidate_requirements'
        ]
        widgets = {
            'company_address': forms.Textarea(attrs={'rows': 3}),
            'preferred_candidate_requirements': forms.Textarea(attrs={'rows': 4}),
        }

class BankDetailsForm(forms.ModelForm):
    class Meta:
        model = BankDetails
        fields = [
            'bank_name',
            'account_number',
            'ifsc_code',
            'account_holder_name',
        ]
        widgets = {
            'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control'}),
            'ifsc_code': forms.TextInput(attrs={'class': 'form-control'}),
            'account_holder_name': forms.TextInput(attrs={'class': 'form-control'}),
        } 