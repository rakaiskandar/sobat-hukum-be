from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    # path('cases/', CaseViewSet.as_view(), name='view_case'),
    path('cases/', CreateCaseView.as_view(), name='create_case'),
    path('cases/<str:case_id>/approve/', ApproveCaseView.as_view(), name='approve_case'),
    path('cases/open/', OpenCasesView.as_view(), name='open_cases'),
    path('cases/<str:case_id>/delete/', DeleteCaseView.as_view(), name='delete_case'),
]
