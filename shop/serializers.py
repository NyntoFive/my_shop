import re
from rest_framework import serializers
from shop.models import Product, Image, Category

class ImageSerializer(serializers.ModelSerializer):
    def clean_spider_data(string_of_urls):
        pattern = re.compile(r"[[]], re.DOTALL")
        if '[' in string_of_urls:
            tmp = string_of_urls.replace('[','')
        if ']' in string_of_urls:
            tmp = string_of_urls.replace(']','')
        if len(tmp) > 0 or '[' not in string_of_urls:
            new = ["https://www.knifekits.com/vcom/images/" + url.strip() for url in tmp.split(',')]
        return new
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
