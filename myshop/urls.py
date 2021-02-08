from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from django.conf import settings
from django.conf.urls.static import static
from shop.serializers import ProductSerializer
from shop.models import Image, Category, Product
from rest_framework import routers, serializers, viewsets
from django.views.generic import TemplateView

from shop.views import ProductViewSet
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']
class ProductList(serializers.ListSerializer):
    model = Product
    queryset =  Product.objects.all()
    serializer_class = ProductSerializer
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'products', ProductViewSet)

class PortfolioView(TemplateView):
    template_name = "index.html"



urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    # path('orders/', include('orders.urls', namespace='orders')),
    # path('payment/', include('payment.urls', namespace='payment')),
    # path('drf/', include(router.urls)),
    path(
        'api-auth/',
        include('rest_framework.urls',
            namespace='rest_framework'
        )
    ),
    path('v1/', ProductViewSet),
    # path('apivi/', include('apiv1.urls')),
    path('portfolio/', PortfolioView.as_view(), name="portfolio",),
    path('', include('shop.urls', namespace='shop')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
