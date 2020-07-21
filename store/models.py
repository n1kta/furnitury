from django.db import models
from django.contrib.auth.models import User


class MinCategory(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True)
    subcategory = models.ManyToManyField(MinCategory)

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True,
        on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=False)
    description = models.TextField(null=True, blank=True)
    quality = models.CharField(max_length=255, null=True, blank=True)
    product_id = models.IntegerField(default=0, null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    subcategory = models.ForeignKey(MinCategory, related_name='p_subcategory',
        null=True, blank=True, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, blank=True,
        on_delete=models.CASCADE)
    image = models.ImageField()
    
    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True, blank=True,
        on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for item in orderitems:
            if not item.product.digital:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderItems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderItems])
        return total

    @property
    def get_cart_items(self):
        orderItems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderItems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True,
        on_delete=models.CASCADE)
    order = models.ForeignKey(Order, null=True, blank=True,
        on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order.transaction_id)

    @property
    def get_total(self):
        return self.product.price * self.quantity


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, null=True, blank=True,
        on_delete=models.CASCADE)
    order = models.ForeignKey(Order, null=True, blank=True,
        on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    phone = models.CharField(max_length=200, null=True)
    orderitems = models.ForeignKey(OrderItem, null=True, blank=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.address)


class MailBox(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    body = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)