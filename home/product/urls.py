from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'viewset', views.ProductViewSet, basename='product-viewset')

urlpatterns = [
    # Demo Function-Based Views (FBVs)
    path('', views.product_list, name='product-list'),
    path('<int:pk>/', views.product_detail, name='product-detail'),
    path('categories/', views.category_list, name='category-list'),
    path('summary/', views.product_summary, name='product-summary'),

    # Demo Generic Class-Based Views (CBVs)
    path('cbv/', views.ProductListCreateAPIView.as_view(), name='product-cbv-list'),
    path('cbv/<int:pk>/', views.ProductDetailAPIView.as_view(), name='product-cbv-detail'),

    # Demo ModelViewSet
    path('api/', include(router.urls)),
]
