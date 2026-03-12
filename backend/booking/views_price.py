from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import PriceHistory, Property
from .serializers import PriceHistorySerializer

@api_view(['GET'])
def property_price_history(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    history = property_obj.price_history.all().order_by('-changed_at')
    serializer = PriceHistorySerializer(history, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def price_history_create(request):
    serializer = PriceHistorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)