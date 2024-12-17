from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh_view'),
    path('token/verify', VerifyTokenView.as_view(), name='token_refresh_view'),
    path('register/', RegisterView.as_view(), name='register'),
    path('clients/create/', CreateClientView.as_view(), name='create_client'),
    path('clients/verify/<str:user_id>/', VerifyClientView.as_view(), name='verify_client'),
    path('lawyers/create/', CreateLawyerView.as_view(), name='create_lawyer'),
    path('lawyers/verify/<str:user_id>/', VerifyLawyerView.as_view(), name='verify_lawyer'),
    path('lawyers/public/', LawyerListPublicView.as_view(), name='lawyer-list'),
    path('lawyers/list/', LawyerListView.as_view(), name='lawyer_list'),
    path('users/', GetUserView.as_view(), name='get_user'),
    path('users/me/', GetUserMeView.as_view(), name='get_user_me'),
    path('users/update/', UpdateProfile.as_view(), name='update_profile'),
    path('users/<str:user_id>/', UserDetailView.as_view(), name='user-detail'),
]