from app.models import User,Profile,FoodLog
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password1=serializers.CharField(write_only=True)
    password2=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['username','email','password','phone','password1','password2']
        read_only_fields=['password']
    def create(self, validated_data):       #validated_data=>username,email,password,password1,password2
        password1=validated_data.pop("password1")
        password2=validated_data.pop("password2")
        if password1!=password2:
            raise serializers.ValidationError("Password mismatched!")
        return User.objects.create_user(**validated_data,password=password1)

class Profileserializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Profile
        fields="__all__"
        read_only_fields=['id','user','daily_calorie_goal','bmi',"created_at"]

class FoodLogSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=FoodLog
        fields="__all__"
        read_only_fields=["id",'user','created_at','updated_at']