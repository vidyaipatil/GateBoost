from django.urls import path
from . import views

app_name = 'tests'

urlpatterns = [
    path('select/', views.test_selection, name='testhome'),
    path('instructions/', views.instructions, name='instructions'),
    path('test/', views.test, name="test"),
    path('revise/', views.revise, name="revise"),
    path('result/', views.result, name="result"),
]