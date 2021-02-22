from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from django.conf import settings
from django.conf.urls.static import static
from shop.serializers import ProductSerializer
from shop.models import Image, Category, Product
from rest_framework import routers, serializers, viewsets
from ninja import NinjaAPI
from blog.api import router as blog_router
from . import views

api = NinjaAPI()
api.add_router('/blog/', blog_router)



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
    path('portfolio/', views.PortfolioView.as_view(), name="portfolio",),
    path('dash/', views.DashboardView.as_view(), name="dash",),
    path('api/', api.urls),
    path('blog/', include('blog.urls')),
    path('chat/', include('chat.urls')),
    path('myphoto/', include('myphoto.urls')),
    path('mydash/', views.MyDashView.as_view()),
    path('', include('shop.urls', namespace='shop')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
