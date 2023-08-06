from django.urls import path, include
from rest_framework import routers
from .views import FilerViewSet, FilerFolderViewSet


router = routers.DefaultRouter()
router.register('api/django-filer/images', FilerViewSet)
router.register('api/django-filer/folders', FilerFolderViewSet)

urlpatterns = [
    path('', include(router.urls))
]