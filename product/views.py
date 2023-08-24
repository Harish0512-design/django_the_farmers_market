from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product, Discount, Cart, CheckOut
from .serializers import ProductSerializer, DiscountSerializer, CartSerializer, CheckOutSerializer
from .checkout3 import CheckOutClass


# Create your views here.
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class DiscountViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer


@api_view(['GET', 'POST'])
def carts_list_view(request):
    if request.method == 'GET':
        items = Cart.objects.all()
        serializer = CartSerializer(items, many=True)
        return Response(serializer.data, status=200)

    elif request.method == 'POST':
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response({'product': "Product doesn't exists"}, status=500)


@api_view(['GET', 'PUT', 'DELETE'])
def carts_detail_view(request, pk):
    try:
        cart_item = Cart.objects.get(pk=pk)
    except Cart.DoesNotExist:
        return Response({'response': '404 NOT FOUND'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CartSerializer(cart_item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CartSerializer(cart_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        cart_item.delete()
        return Response({"response": '204 NO CONTENT'}, status=status.HTTP_204_NO_CONTENT)


def add_to_checkout():
    prod_obj = Cart.objects.values()
    cart = Cart.objects.all()
    dis_obj = Discount.objects.values()
    # print(prod_obj)
    # print(dis_obj)
    prod_details = []
    for p in prod_obj:
        pr = Product.objects.get(pk=p.get('product_id'))
        de = {
            'product_code': pr.product_code,
            'price': float(pr.price)
        }
        # print(de)
        prod_details.append(de)
    dis_details = []
    for d in dis_obj:
        dr = {
            'discount_code': d.get('discount_code'),
            'discount_price': d.get('discount_price')
        }
        dis_details.append(dr)
    # print(prod_details)
    # print(dis_details)
    checkoutobj = CheckOutClass(prod_details, dis_details)

    final_price, discount = checkoutobj.get_final_price_and_discount()
    if float(final_price) > 0:
        data = {'products': prod_details, 'total_discount': float(discount), 'final_price': float(final_price)}
        # print(data)
        serializer = CheckOutSerializer(data=data)
        if serializer.is_valid():
            obj = serializer.save()
            cart.delete()
            return obj.id
    return -1


@api_view(['GET'])
def get_checkout_bill(request):
    if request.method == 'GET':
        pk = add_to_checkout()
        # print(pk)
        if pk > 0:
            checkout_item = CheckOut.objects.get(pk=pk)
            serializer = CheckOutSerializer(checkout_item)
            return Response(serializer.data)
        else:
            return Response({"response": "404 NOT found"}, status=404)
