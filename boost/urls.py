from django.urls import path
from boost import views

app_name = 'boost'
urlpatterns = [
    path('', views.homepage, name='homepage' ),
    path('home/', views.homepage, name='homepage' ),
    path('about/', views.about, name='about' ),
    path('help/', views.help, name='help' ),
]