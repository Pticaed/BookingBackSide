from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Booking
from .serializers import BookingSerializer

@api_view(['GET'])
def booking_list(request):
    queryset = Booking.objects.all()
    guest = request.query_params.get('guest')
    if guest:
        queryset = queryset.filter(guest__wallet_address__iexact=guest)
    serializer = BookingSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def booking_create(request):
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def booking_update(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    serializer = BookingSerializer(booking, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)