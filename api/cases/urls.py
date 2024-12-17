from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    # path('cases/', CaseViewSet.as_view(), name='view_case'),
    path('cases/', CreateCaseView.as_view(), name='create_case'),
    path('cases/<str:case_id>/approve/', ApproveCaseView.as_view(), name='approve_case'),
    path('cases/open/', OpenCasesView.as_view(), name='open_cases'),
    path('cases/assign/', CasesAssignView.as_view(), name='assign_cases'),
    path('cases/<str:case_id>/delete/', DeleteCaseView.as_view(), name='delete_case'),
    path('cases/all/', ListAllCasesView.as_view(), name='list_all_cases'),
    path('cases/history/<str:client_id>/', CaseHistoryView.as_view(), name='case_history'),
    path('cases/count/', CaseCountView.as_view(), name='case_count'),
]
