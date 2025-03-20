from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ssn = models.CharField(max_length=11)  # Store encrypted in production
    filing_status = models.CharField(
        max_length=20,
        choices=[
            ('SINGLE', 'Single'),
            ('MARRIED_JOINTLY', 'Married Filing Jointly'),
            ('MARRIED_SEPARATELY', 'Married Filing Separately'),
            ('HEAD_OF_HOUSEHOLD', 'Head of Household'),
        ]
    )
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField()

    def __str__(self):
        return f"{self.user.get_full_name()}'s Profile"

class Dependent(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='dependents')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    ssn = models.CharField(max_length=11)  # Store encrypted in production
    relationship = models.CharField(max_length=50)
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class TaxDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document_type = models.CharField(
        max_length=20,
        choices=[
            ('W2', 'W-2'),
            ('1099', '1099'),
            ('OTHER', 'Other'),
        ]
    )
    tax_year = models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='tax_documents/')
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('PROCESSING', 'Processing'),
            ('PROCESSED', 'Processed'),
            ('ERROR', 'Error'),
        ],
        default='PENDING'
    )
    extracted_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.document_type} - {self.tax_year} ({self.user.username})"

class TaxReturn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tax_year = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('DRAFT', 'Draft'),
            ('IN_PROGRESS', 'In Progress'),
            ('COMPLETED', 'Completed'),
            ('FILED', 'Filed'),
        ],
        default='DRAFT'
    )
    documents = models.ManyToManyField(TaxDocument)
    total_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    refund_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    filed_date = models.DateTimeField(null=True, blank=True)
    tax_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s {self.tax_year} Tax Return"

    class Meta:
        unique_together = ['user', 'tax_year'] 