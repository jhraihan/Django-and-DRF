from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


# ==========================================
# 1. Function-Based Demo Views (FBVs)
# ==========================================

@api_view(['GET', 'POST'])
def product_list(request):
    """List all products or create a new product."""
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def product_detail(request, pk):
    """Retrieve, update, or delete a single product."""
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method in ('PUT', 'PATCH'):
        partial = request.method == 'PATCH' or True
        serializer = ProductSerializer(product, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def category_list(request):
    """List all categories or create a new category."""
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def product_summary(request):
    """Demo summary endpoint returning quick inventory statistics."""
    total = Product.objects.count()
    available = Product.objects.filter(is_available=True).count()
    out_of_stock = Product.objects.filter(stock=0).count()
    return Response({
        'total_products': total,
        'available_products': available,
        'out_of_stock_products': out_of_stock,
        'total_categories': Category.objects.count(),
    })


# ==========================================
# 2. Generic Class-Based Demo Views (CBVs)
# ==========================================

class ProductListCreateAPIView(generics.ListCreateAPIView):
    """Short generic class-based view for listing and creating products."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Short generic class-based view for retrieving, updating, or deleting a product."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# ==========================================
# 3. ModelViewSet Demo (Full CRUD in 3 lines)
# ==========================================

class ProductViewSet(viewsets.ModelViewSet):
    """Ultra-concise DRF ModelViewSet providing full CRUD operations."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
