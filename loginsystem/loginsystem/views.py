import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return Response({'detail': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'id': user.id, 'email': user.email}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def signin(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return Response({'detail': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)

    email = data.get('email')
    password = data.get('password')
    user = authenticate(username=email, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        })
    return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def me(request):
    user = request.user
    return Response({'id': user.id, 'email': user.email})
