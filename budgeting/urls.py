from django.urls import path
from . import views
from .views import (TransListView, TransDetailView,
                    TransCreateView, TransUpdateView,
                    TransDeleteView)


urlpatterns = [
    path('', TransListView.as_view(), name='budgeting-home'),
    path('transaction/<int:pk>/', TransDetailView.as_view(),
         name='transaction-detail'),
    path(r'transaction/new/?<parameter>', TransCreateView.as_view(),
         name='transaction-create'),
    path('transaction/<int:pk>/update/', TransUpdateView.as_view(),
         name='transaction-update'),
    path('transaction/<int:pk>/delete/', TransDeleteView.as_view(),
         name='transaction-delete'),
    path('about/', views.about, name='budgeting-about')

]
