from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('cases/', CaseViewSet.as_view(), name='view_case'),
    path('document/', DocumentViewSet.as_view(), name='document_view'),
    path('documents/<str:case_id>/', DocumentByCaseView.as_view(), name='documents-by-case'),
    path('case-detail/<str:case_id>/', CaseDetailView.as_view(), name='case-detail'),
    path('case-update/', CreateCaseUpdateView.as_view(), name='create-case-update'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)