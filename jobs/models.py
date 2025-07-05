from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('FULL_TIME', 'Full Time'),
        ('PART_TIME', 'Part Time'),
        ('CONTRACT', 'Contract'),
        ('INTERNSHIP', 'Internship'),
        ('FREELANCE', 'Freelance'),
    ]

    SALARY_RANGE_CHOICES = [
        ('0-20000', '₹0 - ₹20,000'),
        ('20000-50000', '₹20,000 - ₹50,000'),
        ('50000-100000', '₹50,000 - ₹1,00,000'),
        ('100000+', '₹1,00,000+'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    location = models.CharField(max_length=100)
    salary_range = models.CharField(max_length=20, choices=SALARY_RANGE_CHOICES)
    deadline = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SHORTLISTED', 'Shortlisted'),
        ('REJECTED', 'Rejected'),
        ('HIRED', 'Hired'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    cover_letter = models.TextField(blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['job', 'candidate']

    def __str__(self):
        return f"{self.candidate.get_full_name()} - {self.job.title}"
