from django import forms
from django.contrib.auth.models import User
from .models import *
from customer.models import *
class ContactusForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactusForm, self).__init__(*args, **kwargs)
        self.fields['Email'].widget.attrs['placeholder'] = 'Enter a valid E-mail'
    class Meta:
        model = Contact
        fields = [
            'first_name',
            'last_name',
            'Email',
            'subject',
            'message'
        ]

class ContactForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['Email'].widget.attrs['placeholder'] = 'Enter a valid E-mail'

    class Meta:
        model = Contact
        fields = [
            'first_name',
            'last_name',
            'Email',
            'subject',
            'message'
        ]


class JobListingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(JobListingForm, self).__init__(*args, **kwargs)
        self.fields['job_location'].widget.attrs['placeholder'] = 'Harare'
        self.fields['Salary'].widget.attrs['placeholder'] = ' 4k-5k USD, Negotiable'
        self.fields['title'].widget.attrs['placeholder'] = 'Software Engineer, Web Designer'
        self.fields['application_deadline'].widget.attrs['placeholder'] = '2023-08-27'

    class Meta:
        model = JobListing
        exclude = ('user', 'image')
        labels = {
            "job_location": "Job Location",
            "published_on": "Publish Date"
        }



