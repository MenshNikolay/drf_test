from rest_framework import serializers
#from django.contrib.auth.models import User
from rest_framework import serializers
from .models import RefCode, User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email','referral_id','password']
        

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    



class RefCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefCode
        fields = ['ref_code', 'user','creation_date', 'exp_date']    


class RefCodeEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefCode
        fields = ['ref_code']    


class RefUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefCode
        fields = ['referrer']