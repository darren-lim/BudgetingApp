from budgeting.models import Transaction
from rest_framework import viewsets, permissions
from rest_framework import generics
from rest_framework.response import Response
from .serializers import TransactionSerializer

# transaction viewset

class TransactionViewSet(generics.ListAPIView):
    queryset = Transaction.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        user = self.request.user
        # queryset = Transaction.objects.filter(author=user)
        queryset = self.queryset
        return queryset.order_by('date_posted')
