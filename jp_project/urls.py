"""jp_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from jp_app import views
from jp_app.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='index'),
    path('admin_login',admin_login,name='admin_login'),
    path('user_login', user_login, name='user_login'),
    path('recruiter_login', recruiter_login, name='recruiter_login'),
    path('recruiter_signup', recruiter_signup, name='recruiter_signup'),
    path('user_signup', user_signup, name='user_signup'),
    path('user_home', user_home, name='user_home'),
    path('view_user', view_user, name='view_user'),
    path('delete_user/<int:pid>', delete_user, name='delete_user'),
    path('delete_recruiter/<int:pid>', delete_recruiter, name='delete_recruiter'),
    path('admin_home', admin_home, name='admin_home'),
    path('recruiter_pending', recruiter_pending, name='recruiter_pending'),
    path('recruiter_accepted', recruiter_accepted, name='recruiter_accepted'),
    path('recruiter_rejected', recruiter_rejected, name='recruiter_rejected'),
    path('recruiter_home', recruiter_home, name='recruiter_home'),
    path('recruiters_all', recruiters_all, name='recruiters_all'),
    path('change_passwordadmin', change_passwordadmin, name='change_passwordadmin'),
    path('change_passworduser', change_passworduser, name='change_passworduser'),
    path('change_passwordrecruiter', change_passwordrecruiter, name='change_passwordrecruiter'),
    path('change_companylogo/<int:pid>', edit_companylogo, name='edit_companylogo'),
    path('add_job', add_job, name='add_job'),
    path('job_list', job_list, name='job_list'),
    path('user_joblist', user_joblist, name='user_joblist'),
    path('change_status/<int:pid>', change_status, name='change_status'),
    path('home_joblist', home_joblist, name='home_joblist'),
    path('edit_jobdetail/<int:pid>', edit_jobdetail, name='edit_jobdetail'),
    path('job_detail/<int:pid>', job_detail, name='job_detail'),
    path('apply_job/<int:id>',apply_job,name='apply_job'),
    path('candidate_applied',candidate_applied,name='candidate_applied'),
    path('delete_appliation/<int:id>',delete_application,name='delete_application'),
    path('user_appliedjobs',user_appliedjobs,name='user_appliedjobs'),
    path('Logout', Logout, name='Logout'),
    path('contact',contact,name='contact'),
    path('profile',profile,name='profile'),
    path('wishlist',all_wishlist,name='wishlist'),
    path('addWishlist/<int:id>',addWishlist,name='addWishlist'),
    path('deleteWishlist/<int:id>',deleteWishlist,name='deleteWishlist'),
    path('delete_savedjob/<int:id>',delete_savedjob,name='delete_savedjob'),
    path('search',search,name='search')

 ]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
