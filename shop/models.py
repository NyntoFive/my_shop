from django.db import models
from django.urls import reverse

class Image(models.Model):

    fname = models.CharField(max_length=50)
    source = models.URLField(blank=True)
    # position field
    position = models.PositiveSmallIntegerField("Position", null=True)
    class Meta:
        ordering = ['position']
        verbose_name = 'product_image',
        verbose_name_plural = 'product_images'
    
    def __str__(self):
        return self.fname.split('.')[0]

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
    images = models.ForeignKey(
        Image,
        related_name='images',
        on_delete=models.CASCADE
    )
    sku = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True)
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

    
    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
