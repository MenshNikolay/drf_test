from rest_framework import serializers
from django.contrib.auth.models import User
#from drf_app.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

from rest_framework import serializers
from .models import RefCode

class RefCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefCode
        fields = ['ref_code', 'user','creation_date', 'exp_date']    