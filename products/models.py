from django.db import models

from django.core.urlresolvers import reverse

# Create your models here.
# class ProductQuerySet(models.query.QuerySet):
#     def active(self):
#         return self.filter(active = True)
#
# class ProductManager(models.Manager):
#     def get_queryset(self):
#         return ProductQuerySet(self.model, using = self._db)
#
#     def all(self, *args, **kwargs):
#         return self.get_queryset().active()

class Product(models.Model):
    name = models.CharField(primary_key = True, max_length = 50)
    price = models.DecimalField(max_digits = 6, decimal_places = 2)
    sale_price = models.DecimalField(max_digits = 6, decimal_places = 2, blank = True, null = True)
    active = models.BooleanField(default = True)
    # objects = ProductManager()

    PRODUCT_TYPES = (
        ('Top', 'Top'),
        ('Bottom', 'Bottom'),
        ('Hat', 'Hat'),
        ('Shoe', 'Shoe'),
        ('Accessory', 'Accessory'),
    )
    product_type = models.CharField(max_length = 13, choices = PRODUCT_TYPES)
    GENDERS = (
        ('Mens', 'Mens'),
        ('Womens', 'Womens'),
        ('Unisex', 'Unisex'),
    )
    gender = models.CharField(max_length = 6, choices = GENDERS)
    SEASONS = (
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
        ('Fall', 'Fall'),
        ('Winter', 'Winter'),
    )
    season = models.CharField(max_length = 6, choices = SEASONS, blank = True, null = True)

    def __str__(self):
        return self.name

    def get_price(self):
        if self.sale_price is not None:
            return self.sale_price
        else:
            return self.price

class ProductColorVariation(models.Model):
    def image_upload_to(instance, filename):
        name = instance.product.name
        color = instance.color
        basename, file_extension = filename.split('.')
        new_filename = '%s-%s.%s' % (name, color, file_extension)
        return 'products/%s/%s/' % (name, new_filename)

    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to = image_upload_to)
    color = models.CharField(max_length = 25, blank = True, null = True)

    def __str__(self):
        return (self.product.name + ' - ' + self.color)

    def get_url(self):
        return reverse('detail_view', kwargs = {'pk': self.id})

class ProductSizeVariation(models.Model):
    product = models.ForeignKey(ProductColorVariation)
    inventory = models.IntegerField()

    SIZES = (
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('7', 'Size 7'),
        ('8', 'Size 8'),
        ('9', 'Size 9'),
        ('10', 'Size 10'),
        ('11', 'Size 11'),
        ('12', 'Size 12'),
        ('13', 'Size 13'),
    )
    size = models.CharField(max_length = 2, choices = SIZES, blank = True, null = True)

    def __str__(self):
        return (self.product.product.name + ' - ' + self.product.color + ' (' + self.size + ')')

    def get_price(self):
        return self.product.product.get_price()

    def get_url(self):
        return self.product.get_url()

    def add_to_cart(self):
        return "%s/?item=%s&qty=1" %(reverse("cart_view"),self.id)

    def remove_from_cart(self):
        return "%s?item=%s&qty=1&delete=True" %(reverse("cart_view"),self.id)

    def get_name(self):
        return (self.product.product.name + ' (' + self.product.color + ', ' + self.size + ')')
