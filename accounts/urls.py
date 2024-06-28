from django.urls import path
from accounts import views


app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.user_logout, name='logout'),
     path('forget-password/', views.forget_pass, name='forgetpassword'),
]

