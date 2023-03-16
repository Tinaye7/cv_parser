from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.forms import ClearableFileInput
from django import forms
# for deleting media files after record is deleted
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    Email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.first_name


JOB_TYPE = (
    ('Part Time', 'Part Time'),
    ('Full Time', 'Full Time'),
    ('Freelance', 'Freelancer'),
)

CATEGORY = (
    ('Web Design', 'Web Design'),
    ('Graphic Design', 'Graphic Design'),
    ('Web Developing', 'Web Developing'),
    ('Software Engineering', 'Software Engineering'),
    ('HR', 'HR'),
    ('Marketing', 'Marketing'),
)
branch = (
    ('Harare','Harare'),
    ('Bulawayo','Bulawayo'),
    ('Chinhoyi','Chinhoyi'),
    ('Mutare','Mutare')
)

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Any', 'Any'),
)


class JobListing(models.Model):
    job_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             null=True, editable=False, blank=True)
    title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=200)
    employment_status = models.CharField(choices=JOB_TYPE, max_length=10)
    vacancy = models.CharField(max_length=10, null=True)
    gender = models.CharField(choices=GENDER, max_length=30, null=True)
    category = models.CharField(choices=CATEGORY, max_length=30)
    description = models.TextField()
    responsibilities = models.TextField()
    experience = models.CharField(max_length=100)
    job_location = models.CharField(max_length=120, choices=branch)
    Salary = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(blank=True, upload_to='media', null=True)
    application_deadline = models.DateTimeField()
    published_on = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(default=1)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("jobs:job-single", args=[self.id])


class Resume(models.Model):
    resume        = models.FileField('Upload Resumes', upload_to='resumes/')
    name          = models.CharField('Name', max_length=255, null=True, blank=True)
    email         = models.CharField('Email', max_length=255, null=True, blank=True)
    mobile_number = models.CharField('Mobile Number',  max_length=255, null=True, blank=True)
    education     = models.CharField('Education', max_length=255, null=True, blank=True)
    skills        = models.CharField('Skills', max_length=1000, null=True, blank=True)
    company_name  = models.CharField('Company Name', max_length=1000, null=True, blank=True)
    college_name  = models.CharField('College Name', max_length=1000, null=True, blank=True)
    designation   = models.CharField('Designation', max_length=1000, null=True, blank=True)
    experience    = models.CharField('Experience', max_length=1000, null=True, blank=True)
    uploaded_on   = models.DateTimeField('Uploaded On', auto_now_add=True)
    total_experience  = models.CharField('Total Experience (in Years)', max_length=1000, null=True, blank=True)

class UploadResumeModelForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['resume']
        widgets = {
            'resume': ClearableFileInput(attrs={'multiple': True}),
        }

# delete the resume files associated with each object or record
@receiver(post_delete, sender=Resume)
def submission_delete(sender, instance, **kwargs):
    instance.resume.delete(False)
