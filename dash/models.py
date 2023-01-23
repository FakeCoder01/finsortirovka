from django.db import models
from core.models import *

# Create your models here.
class LoanProcess(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="mfi_loan_process_userprofile")
    loan = models.OneToOneField(MFILoan, related_name="mfi_loan_process_loan", on_delete=models.CASCADE)
    filled_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fill_user", blank=True, null=True)

    name_of_the_mfi = models.CharField(max_length=40, blank=True, null=True)
    site_address = models.CharField(max_length=200, blank=True, null=True)
    bin = models.CharField(max_length=20, blank=True, null=True)
    inn = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=20, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    answered_call = models.BooleanField(blank=True, null=True)
    in_russia = models.BooleanField(blank=True, null=True)
    working_calculator = models.BooleanField(blank=True, null=True)
    discount = models.BooleanField(blank=True, null=True)
    leagl_relation = models.CharField(max_length=20, blank=True, null=True)
    product_name = models.CharField(max_length=70, blank=True, null=True)
    min_age = models.IntegerField(blank=True, null=True)
    max_age = models.IntegerField(blank=True, null=True)
    loan_type = models.CharField(max_length=30, blank=True, null=True)
    min_amount = models.FloatField(blank=True, null=True)
    max_amount = models.FloatField(blank=True, null=True)
    rate_type = models.CharField(max_length=30, blank=True, null=True)
    interest_rate = models.FloatField(blank=True, null=True)
    late_payment_penalty = models.FloatField(blank=True, null=True)
    plot_mortgage = models.BooleanField(blank=True, null=True)
    early_payment = models.BooleanField(blank=True, null=True)
    income_source = models.CharField(max_length=50, blank=True, null=True)
    docs = models.ManyToManyField(UploadedDocument, blank=True, null=True)
    schedule_of_payment = models.CharField(max_length=20, blank=True, null=True)
    receive_money_by = models.CharField(max_length=16, blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)

    status = models.CharField(max_length=8, default="Applied")
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.full_name