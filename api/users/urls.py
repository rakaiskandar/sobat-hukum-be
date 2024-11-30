from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh_view'),
    path('token/verify', VerifyTokenView.as_view(), name='token_refresh_view'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserInfoView.as_view(), name='profile'),
    path('clients/', CreateClientView.as_view(), name='create_client'),
    path('lawyers/', CreateLawyerView.as_view(), name='create_lawyer')
]
