from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import re
import uuid

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'uuid', 'username', 'email', 'phone_number', 'first_name', 'last_name']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},  # This makes the password field concealed (hidden) in DRF browsable API
        validators=[validate_password]  # Validate password strength
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = ['email', 'username', 'phone_number', 'password', 'password_confirm']
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'phone_number': {'required': True},
        }

    def validate_phone_number(self, value):
        """Validate phone number format"""
        # Remove spaces, dashes, and parentheses
        phone = re.sub(r'[\s\-\(\)]', '', value)
        # Check if it's a valid phone number (10-15 digits)
        if not re.match(r'^\+?[1-9]\d{9,14}$', phone):
            raise serializers.ValidationError("Invalid phone number format. Use international format: +1234567890")
        return phone

    def validate(self, attrs):
        """Validate that passwords match"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')  # Remove password_confirm from validated_data
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}  # Conceal password in DRF browsable API
    )
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if not email or not password:
            raise serializers.ValidationError("Email and password are required")
        
        return attrs 