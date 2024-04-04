from rest_framework.response import Response
from rest_framework import status, generics,permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, RefCodeSerializer, RefCodeEmailSerializer
from rest_framework.permissions import AllowAny
#from django.contrib.auth.models import User

from drf_app.models import RefCode, User
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
            }, 
            status=status.HTTP_201_CREATED)
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
    

class RefCodeEmailAPIView(generics.CreateAPIView):
    serializer_class = RefCodeEmailSerializer
    authentication_classes = []  
    permission_classes = [AllowAny] 

    def get(self, request, *args, **kwargs):
        ref_user_email = request.query_params.get('ref_user_email', None)
        if not ref_user_email:
            return Response({'error':'We are not able to find such email'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            referrer = User.objects.get(email=ref_user_email)
        except User.DoesNotExist:
            return Response({'error':'User you try to reffer does not exist'}, status=status.HTTP_404_NOT_FOUND)
            
        ref_code = RefCode.objects.filter(user=referrer).first()
        if not ref_code:
            return Response({'error':'It seems this user does not have refferal code'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = RefCodeEmailSerializer(ref_code)
        return Response(serializer.data)
    

class RegesterViaRefCode(generics.CreateAPIView):
        serializer_class = UserSerializer
        authentication_classes = []  
        permission_classes = [AllowAny] 
        
        def create(self, request, *args, **kwargs):
            ref_code = request.data.get('referral_code')
            referrer = RefCode.objects.filter(ref_code=ref_code).first()

            if not referrer:
                return Response({'error':'Ops, you see this mistake because this ref code is invaled either user you refer does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                user.referral_id = referrer
                user.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReferralListView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        referrer_id = self.kwargs['referrer_id']
        return User.objects.filter(referrer_id=referrer_id)
          