from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserListCreateView.as_view(), name='user-list'),
    path('<uuid:uuid>/', views.UserDetailView.as_view(), name='user-detail'),
]
