from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import CustomUserSerializer, RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status



# List all users or create a new one
class UserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all().select_related()  # Optimize queries
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAdminUser]

# Retrieve, update, or delete a single user
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'uuid'


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    http_method_names = ['post']
    throttle_scope = 'register'  # Apply rate limiting

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        data = serializer.data
        # Remove password_confirm from response
        data.pop('password_confirm', None)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return Response(data, status=status.HTTP_201_CREATED)


class LoginView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    http_method_names = ['post']
    throttle_scope = 'login'  # Apply rate limiting

    def create(self, request, *args, **kwargs):
        from django.contrib.auth import authenticate
        
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response(
                {'error': 'Email and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Authenticate user - try email first, then username
        user = None
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            # Try to authenticate with username
            user = authenticate(request, username=email, password=password)
        
        if user is None:
                return Response(
                    {'error': 'Invalid email or password'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        
        if not user.is_active:
            return Response(
                {'error': 'User account is disabled'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'uuid': str(user.uuid),
                'email': user.email,
                'username': user.username,
            }
        }, status=status.HTTP_200_OK)
