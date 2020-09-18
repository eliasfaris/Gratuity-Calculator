from django.contrib import admin
from django.urls import path
from .views import *
from django.urls import include
from .views import home_view
from .views import weekly_report_view

urlpatterns = [
    path('homepage', home_view, name = 'employee_home'), 
    path('', home_view, name = 'employee_home'),
    path('logout', logout_employee,name = 'logoutEmployee'),  
    path('weeklyreports', weekly_report_view, name = "weekly_reports"),
   
]
