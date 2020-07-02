from django.urls import path
from . import views
# from .views import (TransListView, TransDetailView,
#                     TransCreateView, TransUpdateView,
#                     TransDeleteView, HomeView, TotalCreateView)

from .api import CreateTotalAPI,TotalAPI


urlpatterns = [
#     path('', HomeView.as_view(), name='budgeting-home'),
#     path('all_transactions/', TransListView.as_view(), name='all-transactions'),
#     path('enterBalance/', TotalCreateView.as_view(),
#          name='total-create'),
#     path('transaction/<int:pk>/', TransDetailView.as_view(),
#          name='transaction-detail'),
#     path('transaction/new/<str:parameter>/', TransCreateView.as_view(),
#          name='transaction-create'),
#     path('transaction/<int:pk>/update/', TransUpdateView.as_view(),
#          name='transaction-update'),
#     path('transaction/<int:pk>/delete/', TransDeleteView.as_view(),
#          name='transaction-delete'),
#     path('about/', views.about, name='budgeting-about')
     path("total",CreateTotalAPI.as_view()),

]
