from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response

from .models import Total
from .serializers import CreateTotalSerializer,TotalSerializer

class CreateTotalAPI(generics.GenericAPIView):
    serializer_class = CreateTotalSerializer

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        total = serializer.save()
        return Response({
            "total": TotalSerializer(total, context = self.get_serializer_context()).data
        })

    


class TotalAPI(generics.GenericAPIView):
    serializer_class = TotalSerializer

    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_object(self):
        return self.request.total