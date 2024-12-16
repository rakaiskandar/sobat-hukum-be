from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('cases/', CaseViewSet.as_view(), name='view_case'),
    path('document/', DocumentViewSet.as_view(), name='document_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)