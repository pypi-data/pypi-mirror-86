from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from .serializer import FilerSerializer, FilerFolderSerializer
from filer.models import Image, File, Folder


class FilerViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all().order_by('name')
    serializer_class = FilerSerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class FilerFolderViewSet(viewsets.ModelViewSet):
    queryset = Folder.objects.all().order_by('name')
    serializer_class = FilerFolderSerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
