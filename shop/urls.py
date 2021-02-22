from django.urls import path, include
from shop import views
from .apiviews import ProductList, ProductDetail



# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'api', views.ProductViewSet)

app_name = 'shop'

urlpatterns = [
    path('kk/', ProductList.as_view(), name="product_list"),
    path('kk/<int:pk>/', ProductDetail.as_view(), name="product_detail"),
#     path('api/', include(router.urls)),
    path('<int:id>/', views.product_detail, name='product_detail'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('', views.HomepageView.as_view(), name="homepage",),
]

