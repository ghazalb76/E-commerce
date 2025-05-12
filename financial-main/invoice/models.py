from django.db import models
from django.db.models import F

from account.models import Account


class Invoice(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='invoices')
    order_id = models.IntegerField()

    @property
    def total_price(self):
        return sum([item.price * item.quantity for item in self.items.all()])

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     res = super().save(force_insert, force_update, using, update_fields)
    #     Account.objects.filter(pk=self.account_id).update(balance=F('balance') - self.total_price)
    #     return res


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField()
    product_id = models.IntegerField()
    price = models.IntegerField()
