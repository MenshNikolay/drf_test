from rest_framework.response import Response
from rest_framework import status, generics,permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, RefCodeSerializer
from rest_framework.permissions import AllowAny
from drf_app.models import RefCode
from drf_app.utils import gen_ref_code

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    authentication_classes = []  
    permission_classes = [AllowAny] 

    def post(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user) 

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RefCodeInitView(generics.CreateAPIView):
    serializer_class = RefCodeSerializer
    permission_classes = [permissions.IsAuthenticated]



    def post(self, request, *args, **kwargs):
        active_refcode = RefCode.objects.filter(user=request.user).first()
        if active_refcode:
            active_refcode.delete()

        ref_code =  gen_ref_code()
        serializer = self.get_serializer(data={'ref_code': ref_code, 'user':request.user.id})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class RefCodeDestroy(generics.DestroyAPIView):
    serializer_class = RefCodeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return RefCode.objects.get(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        object_to_delete = self.get_object()
        self.perform_destroy(object_to_delete)
        return Response(status=status.HTTP_204_NO_CONTENT)
          