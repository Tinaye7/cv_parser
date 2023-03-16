from . import forms,models
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from customer import models as CMODEL
from customer import forms 
from django.shortcuts import render, redirect, get_object_or_404,get_list_or_404
from .forms import *
from .models import *
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from customer.forms import EmployeeLoginForm
from .models import JobListing
from insurance import forms
from customer.forms import *
from customer.models import *
from django.contrib import messages
from django.db import IntegrityError
from pyresparser import ResumeParser
from customer.models import Resume, UploadResumeModelForm

import os

def home_view(request):
    if request.user.is_authenticated:
        
        return HttpResponseRedirect('afterlogin')  
    return render(request,'insurance/index.html')


def is_customer(user):
    
    return user.groups.filter(name='CUSTOMER').exists()


def afterlogin_view(request):
    qs = JobListing.objects.filter(status = 1)
    jobs = JobListing.objects.all().count()
    user = User.objects.all().count()
    company_name = JobListing.objects.filter(company_name__startswith='P').count()
    paginator = Paginator(qs, 5)  # Show 5 jobs per page
    page = request.GET.get('page')


    
    if is_customer(request.user): 
        try:
            qs = paginator.page(page)
        except PageNotAnInteger:
            qs = paginator.page(1)
        except EmptyPage:
            qs = paginator.page(paginator.num_pages)

        context = {
            'query': qs,
            'job_qs': jobs,
            'company_name': company_name,
            'candidates': user
        }
        return render(request, "customer/home.html", context)
    else:
            try:
                qs = paginator.page(page)
            except PageNotAnInteger:
                qs = paginator.page(1)
            except EmptyPage:
                qs = paginator.page(paginator.num_pages)

            context = {
                'query': qs,
                'job_qs': jobs,
                'company_name': company_name,
                'candidates': user
            }
            return render(request, "insurance/admin_home.html", context)


def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'insurance/contactussuccess.html')
    return render(request, 'insurance/contactus.html', {'form':sub})

def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    query = JobListing.objects.all().count()

    qs = JobListing.objects.all().order_by('-published_on')
    paginator = Paginator(qs, 3)  # Show 3 jobs per page
    page = request.GET.get('page')
    try:
        qs = paginator.page(page)
    except PageNotAnInteger:
        qs = paginator.page(1)
    except EmptyPage:
        qs = paginator.page(paginator.num_pages)

    context = {
        'query': qs,
        'job_qs': query

    }
    return render(request, "insurance/job_listing.html", context)


@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    dict={
        'total_user':CMODEL.Customer.objects.all().count(),
        
    }
    return render(request,'insurance/admin_home.html',context=dict)



@login_required(login_url='adminlogin')
def admin_view_customer_view(request):
    customers= CMODEL.Customer.objects.all()
    return render(request,'insurance/admin_view_customer.html',{'customers':customers})



@login_required(login_url='adminlogin')
def update_customer_view(request,pk):
    customer=CMODEL.Customer.objects.get(id=pk)
    user=CMODEL.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,request.FILES,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('admin-view-customer')
    return render(request,'insurance/update_customer.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_customer_view(request,pk):
    customer=CMODEL.Customer.objects.get(id=pk)
    user=User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return HttpResponseRedirect('/admin-view-customer')


def about_us(request):
    return render(request, "insurance/about_us.html", {})


def service(request):
    return render(request, "insurance/services.html", {})


def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        instance.save()
        return redirect('/')
    context = {
        'form': form
    }
    return render(request, "insurance/contact.html", context)


@login_required
def job_listing(request):
    query = JobListing.objects.all().count()

    qs = JobListing.objects.all().order_by('-published_on')
    paginator = Paginator(qs, 3)  # Show 3 jobs per page
    page = request.GET.get('page')
    try:
        qs = paginator.page(page)
    except PageNotAnInteger:
        qs = paginator.page(1)
    except EmptyPage:
        qs = paginator.page(paginator.num_pages)

    context = {
        'query': qs,
        'job_qs': query

    }
    return render(request, "insurance/job_listing.html", context)


@login_required
def job_post(request):
    form = JobListingForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        instance.save()
        return redirect('/insurance/job-listing')
    context = {
        'form': form,

    }
    return render(request, "insurance/job_post.html", context)


def job_single(request, id):
    job_query = get_object_or_404(JobListing, job_id=id)
    
    job_query.status = 0 # set the new value for the field
    job_query.save() # save the changes to the database
    
    context = {
        'q': job_query,
    }
    return render(request, "insurance/job_single.html", context)


@login_required
def apply_job(request):
    form = JobApplyForm(request.POST or None, request.FILES)
    if form.is_valid():
        instance = form.save()
        instance.save()
        return redirect('/')
    context = {
        'form': form,

    }
    return render(request, "insurance/job_apply.html", context)
@login_required(login_url='adminlogin')
def delete(request,pk):
    model= JobListing
    job_query = get_object_or_404(JobListing, id=id)
    customer=model.objects.get(job_query)
    user=User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return HttpResponseRedirect('/insurance/job-listing')


def admin_login(request):
    next = request.GET.get('next')
    form = EmployeeLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                request.session.set_expiry(420)
                login(request, user)
                return redirect('/')
    context = {
        'form': form
    }
    return render(request, "insurance/admin_login.html", context)

def jobs(request):
    jobs = JobListing.objects.all()
    
    return render(request,'insurance/claims.html',{'joblisting':jobs})

@login_required(login_url='adminlogin')
def assess_job(request,id):
    
    job_query = get_object_or_404(JobListing,job_id=id)
    jobs = ApplyJob.objects.filter(job_id=job_query)
    
    context = {
        'job_query':job_query,
        'jobs': jobs,
       
    }
    
    return render(request, "insurance/assess_job.html", context)

@login_required(login_url='adminlogin')
def assess_applicants(request,pk):
    
    
    customer=ApplyJob.objects.get(apply_id=pk)
    claims = ApplyJob.objects.filter(apply_id=pk)
    #user=models.Licence.objects.get(id=customer.id)
   
    #police = models.PoliceReports.objects.filter(claim_id=customer.id).all()
    #quotation = models.Quotations.objects.filter(claim_id=customer.id).all()
   # damage = models.Damages.objects.filter(claim_id=customer.id).all()
    ClaimsForm=JobApplyForm(instance=customer)
    mydict={'ClaimsForm':ClaimsForm,'claims':claims,}
    if request.method=='POST':
        #licence=JobListing(request.POST,request.FILES)
        #police=models.PoliceReports(request.POST,request.FILES)
        #quotation=models.Quotations(request.POST,request.FILES)
        #damage=models.Damages(request.POST,request.FILES)
        ClaimsForm=JobApplyForm(request.POST,instance=customer)
        if  ClaimsForm.is_valid():
            #user=userForm.save()
            #user.set_password(user.password)
            #user.save()
            ClaimsForm.save()
        return redirect('../jobs')
    return render(request,'insurance/assess_applicants.html',context=mydict)

def homepage(request):
    if request.method == 'POST':
        Resume.objects.all().delete()
        file_form = UploadResumeModelForm(request.POST, request.FILES)
        files = request.FILES.getlist('resume')
        resumes_data = []
        if file_form.is_valid():
            for file in files:
                try:
                    # saving the file
                    resume = Resume(resume=file)
                    resume.save()
                    
                    # extracting resume entities
                    parser = ResumeParser(os.path.join(settings.MEDIA_ROOT, resume.resume.name))
                    data = parser.get_extracted_data()
                    resumes_data.append(data)
                    resume.name               = data.get('name')
                    resume.email              = data.get('email')
                    resume.mobile_number      = data.get('mobile_number')
                    if data.get('degree') is not None:
                        resume.education      = ', '.join(data.get('degree'))
                    else:
                        resume.education      = None
                    resume.company_names      = data.get('company_names')
                    resume.college_name       = data.get('college_name')
                    resume.designation        = data.get('designation')
                    resume.total_experience   = data.get('total_experience')
                    if data.get('skills') is not None:
                        resume.skills         = ', '.join(data.get('skills'))
                    else:
                        resume.skills         = None
                    if data.get('experience') is not None:
                        resume.experience     = ', '.join(data.get('experience'))
                    else:
                        resume.experience     = None
                    resume.save()
                except IntegrityError:
                    messages.warning(request, 'Duplicate resume found:', file.name)
                    return redirect('evaluator')
            resumes = Resume.objects.all()
            messages.success(request, 'Resumes Evaluated!')
            context = {
                'resumes': resumes,
            }
            return render(request, 'insurance/base.html', context)
    else:
        form = UploadResumeModelForm()
    return render(request, 'insurance/base.html', {'form': form})