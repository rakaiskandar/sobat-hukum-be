from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from .views import RegisterView, LoginView, AdminOnlyView

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('admin-only/', AdminOnlyView.as_view(), name='admin-only'),
]
