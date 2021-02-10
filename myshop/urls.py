from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from django.conf import settings
from django.conf.urls.static import static
from shop.serializers import ProductSerializer
from shop.models import Image, Category, Product
from rest_framework import routers, serializers, viewsets
from django.views.generic import TemplateView

from ninja import NinjaAPI
from blog.api import router as blog_router

api = NinjaAPI()
api.add_router('/blog/', blog_router)

class PortfolioView(TemplateView):
    template_name = "index.html"



urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    # path('orders/', include('orders.urls', namespace='orders')),
    # path('payment/', include('payment.urls', namespace='payment')),
    path(
        'api-auth/',
        include('rest_framework.urls',
            namespace='rest_framework'
        )
    ),
    path('portfolio/', PortfolioView.as_view(), name="portfolio",),
    path('api/', api.urls),
    path('blog/', include('blog.urls')),
    path('myphoto/', include('myphoto.urls')),
    path('', include('shop.urls', namespace='shop')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
