from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Image
from django.contrib.auth.models import User
from cart.forms import CartAddProductForm

from rest_framework.reverse import reverse
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view
from rest_framework import viewsets

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    ProductSerializer
)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'products': reverse('product_list_by_category', request=request, format=format)
    })

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()

    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    `Product "list" and "retreive" functions`
    '''
    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# def homepage(request):
#     kits = Product.objects.filter(category=1)
#     return render(request, template_name="shop/homepage.html", context={"kits":kits})

class HomepageView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    queryset = Product.objects.filter(category=1)[:5]
    template_name = 'shop/homepage.html'

    def get(self, request):
        queryset = Product.objects.last()
        return Response({'products': queryset})