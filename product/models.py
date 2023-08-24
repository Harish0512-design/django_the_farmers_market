from django.db import models


# Create your models here.
class Product(models.Model):
    product_code = models.CharField(max_length=8)
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return "%s -- %s" % (self.product_code, self.name)


class Discount(models.Model):
    discount_code = models.CharField(max_length=10)
    discount_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return "%s -- %s" % (self.discount_code, self.discount_price)


class Cart(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.product


class CheckOut(models.Model):
    products = models.JSONField()
    total_discount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    final_price = models.DecimalField(max_digits=15, decimal_places=2, null=False, blank=False)

    def __str__(self):
        return "%s" % self.products
