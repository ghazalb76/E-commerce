from django.db import models


class Order(models.Model):
    user_id = models.IntegerField()
    status = models.CharField(choices=(
        ('completed', 'completed'),
        ('canceled', 'canceled'),
    ),
        max_length=20,
    )
    date = models.DateTimeField(auto_now_add=True)
    total = models.FloatField()


class Cart(models.Model):
    user_id = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    status = models.CharField(
        choices=(
            ('active', 'active'),
            ('ordered', 'ordered'),
        ),
        max_length=20,
    )


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product_id = models.IntegerField()
    quantity = models.IntegerField()
    price = models.FloatField()
