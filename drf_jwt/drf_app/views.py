from urllib import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny

class RegisterView(APIView):
    
    #serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user) # Создание Refesh и Access

            refresh.payload.update({    # Полезная информация в самом токене

                'user_id': user.id,

                'username': user.username

            })
            return Response({

                'refresh': str(refresh),

                'access': str(refresh.access_token), # Отправка на клиент

            }, status=status.HTTP_201_CREATED)
    
