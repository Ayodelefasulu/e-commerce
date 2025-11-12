from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('', views.UserListCreateView.as_view(), name='user-list'),
    path('<uuid:uuid>/', views.UserDetailView.as_view(), name='user-detail'),
    
]
