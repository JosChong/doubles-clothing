from django.db import models

from django.conf import settings
from django.db.models.signals import pre_save, post_save, post_delete

from decimal import Decimal

from products.models import ProductSizeVariation

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank = True, null = True)
    items = models.ManyToManyField(ProductSizeVariation, through = 'CartItem')
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated = models.DateTimeField(auto_now_add = False, auto_now = True)
    subtotal = models.DecimalField(max_digits = 50, decimal_places = 2, default = 0.00)
    tax_percentage = models.DecimalField(max_digits = 50, decimal_places = 2, default = 0.09)
    tax_total = models.DecimalField(max_digits = 50, decimal_places = 2, default = 0.00)
    total = models.DecimalField(max_digits = 50, decimal_places = 2, default = 0.00)

    def __str__(self):
        return str(self.id)

    def update_subtotal(self):
        print("updating...")
        subtotal = 0
        items = self.cartitem_set.all()
        for item in items:
            subtotal += item.item_total
        self.subtotal = subtotal
        self.save()

def tax_total_receiver(sender, instance, *args, **kwargs):
    subtotal = instance.subtotal
    tax_total = round(subtotal * instance.tax_percentage, 2)
    total = round(subtotal + tax_total, 2)
    instance.tax_total = tax_total
    instance.total = total

pre_save.connect(tax_total_receiver, sender = Cart)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart)
    item = models.ForeignKey(ProductSizeVariation)
    quantity = models.PositiveIntegerField(default = 1)
    item_total = models.DecimalField(max_digits = 10, decimal_places = 2)

    def __str__(self):
        return self.item

    def remove(self):
        return self.item.remove_from_cart()

def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
	qty = instance.quantity
	if int(qty) >= 1:
		price = instance.item.get_price()
		item_total = Decimal(qty) * Decimal(price)
		instance.item_total = item_total

def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
    instance.cart.update_subtotal()

pre_save.connect(cart_item_pre_save_receiver, sender = CartItem)

post_save.connect(cart_item_post_save_receiver, sender = CartItem)

post_delete.connect(cart_item_post_save_receiver, sender = CartItem)
