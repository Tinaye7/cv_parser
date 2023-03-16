from django import forms
from django.contrib.auth.models import User
from .models import *
from . import models
from .models import Customer
from django.contrib.auth import authenticate, get_user_model

class CustomerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password',]
        widgets = {
        'password': forms.PasswordInput()
        }



User = get_user_model()

class CustomerForm(forms.ModelForm):
    class Meta:
        model=models.Customer
        fields=['mobile','address']

class EmployeeRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=10)
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    email = forms.EmailField(label='Email address')
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [

            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'confirm_password',

        ]

    def __init__(self, *args, **kwargs):
        super(EmployeeRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Enter a valid e-mail'


class EmployeeLoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(EmployeeLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        return super(EmployeeLoginForm, self).clean(*args, **kwargs)
    
    class Meta:
        model=models.Customer
        fields=['profile_pic','mobile','address']

class JobApplyForm(forms.ModelForm):
    class Meta:
        model = ApplyJob
        fields = ['status','remarks']
        exclude = ['file','applicant','job','apply_id','name','email','phone','application_date']
    