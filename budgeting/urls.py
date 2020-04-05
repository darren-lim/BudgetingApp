from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='budgeting-home'),
    path('about/', views.about, name='budgeting-about')
]
