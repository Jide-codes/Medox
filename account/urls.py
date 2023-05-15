from django.urls import path
from . import views

app_name='account'

urlpatterns = [
    path('login', views.login_page, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('register', views.register_page, name='register')
]
