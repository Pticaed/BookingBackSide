from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Review, Booking
from .serializers import ReviewSerializer

@api_view(['GET'])
def booking_reviews(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    reviews = booking.reviews.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def review_create(request):
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    serializer = ReviewSerializer(review, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    review.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)