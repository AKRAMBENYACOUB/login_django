from django.contrib import admin
from django.urls import path, include

from myapp.views import (
    sing_in, sing_up, dashboard, log_out,
    forgot_password, update_password,send_mail_awsuga
)
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('login', sing_in, name='sing_in'),
    path('register', sing_up, name='sing_up'),
    path('logout', log_out, name='log_out'),
    path('sendmail', send_mail_awsuga, name='send_mail_awsuga'),
    
    path('forgot-password', forgot_password, name='forgot_password'),
    path('update-password/<str:token>/<str:uid>/', update_password, name='update_password'),
]


