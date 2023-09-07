from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),


    path('register-link/', views.register_link, name="register-link"),
    path('user-role/', views.user_role, name="user-role"),
    path('user-register', views.user_register, name="user-register"),
    path('user-login/', views.user_login, name="user-login"),
    path('user-logout/', views.user_logout, name="user-logout"),


    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('reset-password-validate/<uidb64>/<token>/',
         views.resetpassword_validate, name='resetpassword-validate'),
    path('reset-password/', views.reset_password, name='reset-password'),


    path('after-login-page/', views.after_login_page, name='feed'),
    path('my-network/', views.my_network, name='my-network'),





]
