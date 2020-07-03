from budgeting.models import Transaction, History, Total
from rest_framework import viewsets, permissions
from rest_framework import generics
from rest_framework.response import Response
from .serializers import TransactionSerializer, TotalSerializer, HistorySerializer

# transaction viewset

class TransactionViewSet(generics.ListAPIView):
    queryset = Transaction.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        # user = self.request.user
        # queryset = Transaction.objects.filter(author=user)
        # queryset = self.queryset
        return self.queryset.order_by('date_posted')


class TotalViewSet(viewsets.ModelViewSet):
    queryset = Total.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = TotalSerializer


class HistoryViewSet(viewsets.ModelViewSet):
    queryset = History.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = HistorySerializer