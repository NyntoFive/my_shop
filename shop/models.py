from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE,
        
    )
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    sku = models.CharField(max_length=255, unique=True)
    all_images = models.TextField(blank=True)
    cannonical_url = models.URLField()
    video_url = models.URLField(blank=True)
    price = models.CharField(max_length=20)
    keywords = models.CharField(max_length=255, blank=True)
    link = models.URLField()
    discount_tiers = models.CharField(max_length=100, blank=True)
    discount_amount = models.CharField(max_length=100, blank=True)

    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sku

class Image(models.Model):
    fname = models.CharField(max_length=50)

    Product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    # position field
    position = models.PositiveSmallIntegerField("Position", null=True)
    class Meta:
        ordering = ['position']