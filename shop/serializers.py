from rest_framework import serializers
from shop.models import Product, Image, Category

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'
class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = '__all__'
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=True)
    images = ImageSerializer(required=True)
    class Meta:
        model = Product
        fields = '__all__'
