from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    # path('cases/', CaseViewSet.as_view(), name='view_case'),
    path('cases/', CreateCaseView.as_view(), name='create_case'),
]
