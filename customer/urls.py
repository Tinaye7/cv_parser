from django.urls import path
from customer.views import *
from django.contrib.auth.views import LoginView
app_name = 'customer'
urlpatterns = [
    path('customerclick', customerclick_view,name='customerclick'),
    path('customersignup', customer_signup_view,name='customersignup'),
    path('home', customer_dashboard_view,name='applicant-home'),
    path('customerlogin', LoginView.as_view(template_name='customer/customerlogin.html'),name='customerlogin'),
    path('contact/', contact, name='contact'),
    path('about/', about_us, name='about'),
    path('service/', service, name='service'),
    path('job-post/', job_post, name='job-post'),
    path('customer/job-listing', job_listing, name='job-listing'),
    path('job-single/<int:id>/', job_single, name='job-single'),
    path('search/', SearchView.as_view(), name='search'),
    path('apply/<int:id>', apply_job, name='apply'),
    path('apply_job_save/<int:id>', apply_job_save, name='apply_job_save'),
    #path('afterlogin', afterlogin_view,name='afterlogin'),
    #path('customer/afterlogin', afterlogin_view,name='afterlogin'),
    path('customerlogin/', customer_login, name='customer_login'),
    path('applied_jobs/<int:user_id>/jobs/', applied_jobs, name='applied'),
]