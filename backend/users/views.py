from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .serializers import UserSerializer

User = get_user_model()

@api_view(['GET'])
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response({'users': serializer.data})

@api_view(['GET'])
def user_detail(request, wallet_address):
    user = get_object_or_404(User, wallet_address=wallet_address)
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['POST'])
def user_create(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        password = request.data.get('password')
        if password:
            serializer.validated_data['password'] = make_password(password)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
def user_update(request, wallet_address):
    user = get_object_or_404(User, wallet_address=wallet_address)
    partial = True if request.method == 'PATCH' else False
    serializer = UserSerializer(user, data=request.data, partial=partial)
    
    if serializer.is_valid():
        password = request.data.get('password')
        if password:
            user.password = make_password(password)
            user.save()
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def user_delete(request, wallet_address):
    user = get_object_or_404(User, wallet_address=wallet_address)
    user.delete()
    return Response({'message': 'User deleted'}, status=status.HTTP_204_NO_CONTENT)