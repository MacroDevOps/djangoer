from django.shortcuts import render
from rest_framework import viewsets

from book.models import Book
from book.serializer import BookModelsSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookModelsSerializer

