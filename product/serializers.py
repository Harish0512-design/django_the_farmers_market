from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from .models import Discount, Cart, Product, CheckOut


class DiscountSerializer(ModelSerializer):
    class Meta:
        model = Discount
        fields = "__all__"


class CartSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CheckOutSerializer(ModelSerializer):
    class Meta:
        model = CheckOut
        fields = "__all__"
