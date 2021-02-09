from rest_framework import generics

from .models import Product, Category, Image
from .serializers import ProductSerializer, ImageSerializer, CategorySerializer


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    class Meta:
        ordering = ['id']
class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer