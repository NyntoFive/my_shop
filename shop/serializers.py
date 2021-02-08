from rest_framework.serializers import ModelSerializer
from shop.models import Product, Image, Category

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'category_id',
            'images_id',
            'sku',
            'title',
            'name',
            'slug',
            'description',
            'all_images',
            'cannonical_url',
            'video_url',
            'price',
            'keywords',
            'link',
            'discount_tiers',
            'discount_amount',
            'available',
            'created',
            'updated'
        ]

