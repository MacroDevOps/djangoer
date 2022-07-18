from django.shortcuts import render
from rest_framework import viewsets

from book.models import Book, BookFactory
from book.serializer import BookModelsSerializer, BookFactorySerializer


class BookFactoryViewSet(viewsets.ModelViewSet):
    queryset = BookFactory.objects.all()
    serializer_class = BookFactorySerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookModelsSerializer

