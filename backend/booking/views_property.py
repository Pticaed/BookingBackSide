from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Property
from .serializers import PropertySerializer

@api_view(['GET'])
def property_list(request):
    queryset = Property.objects.filter(is_active=True)
    city = request.query_params.get('city')
    country = request.query_params.get('country')
    if city:
        queryset = queryset.filter(city__iexact=city)
    if country:
        queryset = queryset.filter(country__iexact=country)
        
    serializer = PropertySerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    serializer = PropertySerializer(property_obj)
    return Response(serializer.data)

@api_view(['POST'])
def property_create(request):
    serializer = PropertySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def property_update(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    serializer = PropertySerializer(property_obj, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def property_delete(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    property_obj.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def property_availability(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    check_in = request.query_params.get('check_in')
    check_out = request.query_params.get('check_out')
    
    if not check_in or not check_out:
        return Response({'error': 'Dates required'}, status=status.HTTP_400_BAD_REQUEST)
    
    is_available = not property_obj.bookings.filter(
        status='confirmed',
        check_in__lt=check_out,
        check_out__gt=check_in
    ).exists()
    
    return Response({'is_available': is_available})