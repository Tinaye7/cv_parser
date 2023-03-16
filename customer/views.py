from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from insurance import models as CMODEL
from django.conf import settings
from django.core.mail import send_mail
from customer.forms import *
from customer.models import *
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.contrib.auth import authenticate, get_user_model, login, logout
from insurance.models import JobListing
from insurance.forms import *
from customer.models import Customer

def customerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'customer/customerclick.html')
def customer_login(request):
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
    return render(request, "customer/customerlogin.html", context)

def customer_signup_view(request):
    userForm=CustomerUserForm()
    customerForm=CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=CustomerUserForm(request.POST)
        customerForm=CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('customerlogin')
    return render(request,'customer/customersignup.html',context=mydict)

def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()

@login_required(login_url='customerlogin')
def customer_dashboard_view(request):
    dict={
        
        'customer':Customer.objects.get(user_id=request.user.id),
       

    }
    return render(request,'customer/home.html',context=dict)

def about_us(request):
    return render(request, "customer/about_us.html", {})


def service(request):
    return render(request, "customer/services.html", {})


def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        instance.save()
        return redirect('/')
    context = {
        'form': form
    }
    return render(request, "customer/contact.html", context)


@login_required
def job_listing(request):
    query = JobListing.objects.all().count()

    qs = JobListing.objects.filter(status = 1).order_by('-published_on')
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
    return render(request, "customer/job_listing.html", context)


@login_required
def job_post(request):
    form = JobListingForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        instance.save()
        return redirect('/customer/job-listing')
    context = {
        'form': form,

    }
    return render(request, "customer/job_post.html", context)


def job_single(request, id):
    job_query = get_object_or_404(JobListing, job_id=id)

    context = {
        'q': job_query,
    }
    return render(request, "customer/job_single.html", context)


@login_required
def apply_job(request,id):
    job_query = get_object_or_404(JobListing, job_id=id)
    context={
        
        'q':job_query,
    }
    return render(request,'customer/job_apply.html',context)
@csrf_exempt
def apply_job_save(request,id):
    
    job_query = get_object_or_404(JobListing, job_id=id)
    context={
        
        'q':job_query,
    }
    if request.method!="POST":
            return render(request,'customer/job_apply.html',context)
    else:
            job_query = get_object_or_404(JobListing, job_id=id)
            context={
        
            'q':job_query,
                    }
            applicant = Customer.objects.get(user_id=request.user.id)
            name = request.POST.get("name")
            phone = request.POST.get("phone")
            email = request.POST.get("email")

            file1=request.FILES['file1']
            print(file1)
            if (name=="") & (email=="") & (phone==""):
               messages.error(request,"Please fill out all sections")
               return render(request,'customer/job_apply.html',context)
    
            try:
                
                
                fs=FileSystemStorage()
                file_path=fs.save(file1.name,file1)
                
                joblisting=ApplyJob(job=job_query,applicant=applicant,file=file_path,name=name,email=email,phone=phone)
                joblisting.save()
                    
                messages.success(request,"Data Saved Successfully")
                return render(request,'customer/job_apply.html',context)
            
            except:
                messages.error(request,"Error in Applying for Job")
                return render(request,'customer/job_apply.html',context)

@login_required(login_url='adminlogin')
def delete(request,pk):
    model= JobListing
    job_query = get_object_or_404(JobListing, id=id)
    customer=model.objects.get(job_query)
    user=User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return HttpResponseRedirect('/customer/job-listing')

class SearchView(ListView):
    model = JobListing
    template_name = 'customer/search.html'
    context_object_name = 'customer'

    def get_queryset(self):
        return self.model.objects.filter(title__contains=self.request.GET['title'],
                                         job_location__contains=self.request.GET['job_location'],
                                         employment_status__contains=self.request.GET['employment_status'])
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
    return render(request, "customer/customerlogin.html", context)



def applied_jobs(request,user_id):
    customer = Customer.objects.get(user_id=user_id)
    #job_id= JobListing.objects.get(id=id)
    jobs = ApplyJob.objects.filter(applicant=customer)
    applied=[]
    for job in jobs:
        joob  = JobListing.objects.get(pk=job.job.job_id)
        applied.append(joob)
    context={
                #'customer': customer,
                #'job_id':job_id,
                'applied':applied,
                'jobs':jobs
                }
    return render(request,'customer/applied_jobs.html',context)