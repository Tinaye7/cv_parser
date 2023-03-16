from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from insurance.models import *
from django import forms
from django.forms import ClearableFileInput
status=(
            ('Approved','APPROVED'),
            ('Rejected','REJECTED'),
            ('Pending','PENDING'),
        )
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name



class UploadResumeModelForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['resume']
        widgets = {
            'resume': ClearableFileInput(attrs={'multiple': True}),
        }

class ApplyJob(models.Model):
    apply_id= models.AutoField(primary_key=True)
    applicant=models.ForeignKey(Customer,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=11,null=False)
    email = models.EmailField()
    file = models.FileField(null=True)
    application_date = models.DateTimeField(default=timezone.now)
    job= models.ForeignKey(JobListing,on_delete=models.CASCADE)
    status = models.CharField(max_length=255,choices=status,default='Pending')
    remarks = models.CharField(max_length=255,default='Pending Assessment')
    objects=models.Manager()