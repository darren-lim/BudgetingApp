from django.urls import path



from .api import TransactionViewSet


urlpatterns = [
     path('all_transactions/', TransactionViewSet.as_view()),
]
