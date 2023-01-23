from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userprofile")
    p_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    full_name = models.CharField(max_length=70, blank=True, null=True)
    gender = models.CharField(max_length=8, blank=True, null=True)
    phone = models.CharField(max_length=13, blank=True, null=True)
    address = models.TextField(null=True, blank=True)
    profile_active = models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.full_name 

class UploadedDocument(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="document_loan_profile")
    doc_id = models.CharField(max_length=6, default=get_random_string(6), unique=True)
    document_name = models.CharField(max_length=60, null=True, blank=True)
    media = models.FileField(upload_to='Documents/')        
    def __str__(self) -> str:
        return self.profile.full_name + f' ({self.document_name})'

class MFILoan(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="mfi_loan_userprofile")
    loan_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    legal_status_of_user = models.CharField(max_length=40)
    confirm_income_source = models.CharField(max_length=150)
    age_of_user = models.IntegerField()
    loan_amount = models.BigIntegerField()
    loan_tenure_in_days = models.IntegerField()
    loan_type = models.CharField(max_length=20)
    documents = models.ManyToManyField(UploadedDocument, blank=True, null=True)
    method_of_receiving_money = models.CharField(max_length=160)
    region = models.CharField(max_length=50)
    message = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.full_name