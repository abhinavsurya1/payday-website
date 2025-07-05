from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, RegexValidator
from django.utils import timezone

class UserRegistrationType(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='registration_type')
    type = models.CharField(max_length=20, choices=[('client', 'Client'), ('candidate', 'Candidate')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.type}"

class CandidateProfile(models.Model):
    JOB_TYPE_CHOICES = [
        ('FULL_TIME', 'Full Time'),
        ('PART_TIME', 'Part Time'),
        ('CONTRACT', 'Contract'),
        ('INTERNSHIP', 'Internship'),
        ('FREELANCE', 'Freelance'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')],
        help_text='Enter your primary contact number'
    )
    whatsapp_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')],
        blank=True,
        null=True,
        help_text='Optional: For faster communication with employers'
    )
    date_of_birth = models.DateField()
    address = models.TextField()
    preferred_job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    skills = models.TextField(help_text='List your key skills, separated by commas')
    experience = models.TextField(help_text='Describe your work experience and achievements')
    
    # Document fields
    cv = models.FileField(
        upload_to='candidates/cv/',
        help_text='Upload your CV in PDF or Word format'
    )
    profile_picture = models.ImageField(
        upload_to='candidates/profile_pictures/',
        help_text='Upload a professional headshot'
    )
    additional_pictures = models.ImageField(
        upload_to='candidates/additional_pictures/',
        blank=True,
        null=True,
        help_text='Optional: Upload additional professional pictures'
    )
    photo_id = models.ImageField(
        upload_to='candidates/photo_id/',
        help_text='Upload your photo ID for verification'
    )
    
    # Status fields
    is_verified = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()}'s Profile"

    def save(self, *args, **kwargs):
        # Check if all required fields are filled
        required_fields = [
            self.phone_number,
            self.date_of_birth,
            self.address,
            self.preferred_job_type,
            self.skills,
            self.experience,
            self.cv,
            self.profile_picture,
            self.photo_id
        ]
        self.is_complete = all(required_fields)
        super().save(*args, **kwargs)

class ClientProfile(models.Model):
    INDUSTRY_CHOICES = [
        ('TECH', 'Technology'),
        ('HEALTHCARE', 'Healthcare'),
        ('RETAIL', 'Retail'),
        ('HOSPITALITY', 'Hospitality'),
        ('EVENTS', 'Events'),
        ('OTHER', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    company_name = models.CharField(max_length=200)
    industry = models.CharField(max_length=20, choices=INDUSTRY_CHOICES)
    gst_number = models.CharField(max_length=15, unique=True)
    company_address = models.TextField()
    phone_number = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15, blank=True)
    company_website = models.URLField(blank=True)
    company_logo = models.ImageField(
        upload_to='clients/logos/',
        blank=True,
        help_text='Upload your company logo'
    )
    preferred_candidate_requirements = models.TextField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

class VerificationDocument(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('GST', 'GST Certificate'),
        ('PAN', 'PAN Card'),
        ('INCORP', 'Incorporation Certificate'),
        ('OTHER', 'Other'),
    ]

    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='verification_documents')
    document_type = models.CharField(max_length=10, choices=DOCUMENT_TYPE_CHOICES)
    document = models.FileField(
        upload_to='clients/verification_documents/',
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])],
        help_text='Upload verification document'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.client.company_name} - {self.document_type}"

class BankDetails(models.Model):
    candidate_profile = models.OneToOneField(
        CandidateProfile,
        on_delete=models.CASCADE,
        related_name='bank_details'
    )
    bank_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=255)
    ifsc_code = models.CharField(max_length=11) # IFSC codes are typically 11 characters
    account_holder_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.account_holder_name}'s Bank Details"
