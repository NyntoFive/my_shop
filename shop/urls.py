from django.urls import path, include
from rest_framework.routers import DefaultRouter
from shop import views

router = DefaultRouter()
router.register(r'api', views.ProductViewSet)

app_name = 'shop'

urlpatterns = [
    path('api/', include(router.urls)),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('', views.homepage, name="homepage",),
]
