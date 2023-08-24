from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, DiscountViewSet, carts_list_view, carts_detail_view, get_checkout_bill

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'discounts', DiscountViewSet, basename='discounts')

urlpatterns = [
    path('', include(router.urls)),
    path('carts/', carts_list_view),
    path('carts/<int:pk>', carts_detail_view),
    path('checkout/', get_checkout_bill),
]
