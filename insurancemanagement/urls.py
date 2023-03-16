
from django.contrib import admin
from django.urls import path
from insurance import views
from django.contrib.auth.views import LogoutView,LoginView
from django.urls import path,include
from insurance.views import *
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),


    path('customer/',include('customer.urls', namespace='customer')),
    path('',views.home_view,name='home'),
    path('logout', LogoutView.as_view(template_name='insurance/logout.html'),name='logout'),
    
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('customer/afterlogin', views.afterlogin_view,name='afterlogin'),
     path('contactus', views.contactus_view),
    path('adminlogin', LoginView.as_view(template_name='insurance/adminlogin.html'),name='adminlogin'),
    path('insurance/admin_home', views.admin_dashboard_view,name='admin_home'),

    path('admin-view-customer', views.admin_view_customer_view,name='admin-view-customer'),
    path('update-customer/<int:pk>', views.update_customer_view,name='update-customer'),
    path('delete-customer/<int:pk>', views.delete_customer_view,name='delete-customer'),
    path('contact/', contact, name='contact'),
    path('about/', about_us, name='about'),
    path('service/', service, name='service'),
    path('job-post/', job_post, name='job-post'),
    path('insurance/job-listing', job_listing, name='job-listing'),
    path('job-single/<int:id>/', job_single, name='job-single'),
    path('jobs',jobs, name='job-applications'),
    path('apply/', apply_job, name='apply'),
    path('admin_login/', admin_login, name='admin_login'),
    path('assess_job/<int:id>/', assess_job,name='assess_job'),
    path('delete/<int:pk>', views.delete,name='delete'),
    path('assess_applicants/<int:pk>',views.assess_applicants,name='assess_applicants'),
     path('evaluator/', views.homepage, name='evaluator'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
