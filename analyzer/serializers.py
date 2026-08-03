from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ResumeAnalysis

class ResumeUploadSerializer(serializers.Serializer):
    job_description = serializers.CharField(required=False, allow_blank=True)
    resume = serializers.FileField()

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # Creates a new user with an encrypted password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user