from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

from random import randint


# категорія продукту
class Category(models.Model):
    field = models.CharField(max_length=50)

    def __str__(self):
        return 'Category: {}'.format(self.field)


# Клас продукту
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField()
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    brand = models.CharField(max_length=50)
    weight = models.PositiveIntegerField()
    old_price = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    slug = models.CharField(max_length=100, unique=True, blank=True)
    stock = models.CharField(max_length=25, default='В наявності')

    def get_absolute_url(self):
        return reverse('Product_information_url', kwargs={'slug': self.slug})

    def __str__(self):
        return '{}'.format(self.title)

    def save(self, *args, **kwargs):
        alpha = {
            'a': 'a', 'б': 'b', 'ц': 'c', 'д': 'd', 'е': 'e', 'ф': 'f', 'г': 'g', 'х': 'h', 'і': 'i', 'й': 'j', 'к': 'k',
            'л': 'l', 'м': 'm', 'н': 'n', 'п': 'p', 'о': 'o', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'в': 'v', 'и': 'y',
            'з': 'z', 'щ': 'sch', 'ш': 'ch', 'я': 'yi', 'ь': '', 'ж': 'sh', ' ': '-'}

        invalid_slug = str(randint(0, 1000)) + '-' + str(self.title) + '-' + str(self.brand) + '-' + str(self.weight)
        invalid_slug = invalid_slug.lower()

        for key, value in alpha.items():
            for i in invalid_slug:
                if key == i:
                    invalid_slug = invalid_slug.replace(i, value)
        self.slug = invalid_slug
        super(Product, self).save(*args, **kwargs)


# Екземпляр коментаря
class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=50)
    user_email = models.EmailField(max_length=50)
    message = models.TextField(max_length=200)
    date_pub = models.DateTimeField(default=timezone.now)


# Клас, екземпляри якого будуть відігравати роль корзини
class Basket(models.Model):
    session_key = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    id_product = models.IntegerField()
    image = models.ImageField()
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    number = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return '{}'.format(self.title)

    def save(self, *args, **kwargs):
        self.total_price = self.price * self.number
        super(Basket, self).save(*args, **kwargs)


# Клас замовдення
class Order(models.Model):

    STATUS = (
        ('В роботі', 'В роботі'),
        ('Опрацьовано', 'Опрацьовано')
    )

    session_key = models.CharField(max_length=100)
    user_status = models.BooleanField(default=False)
    buyer_name = models.CharField(max_length=15)
    buyer_lastname = models.CharField(max_length=25)
    buyer_tel = models.CharField(max_length=17)
    buyer_email = models.EmailField(max_length=30)
    pay_way = models.CharField(max_length=25)
    transporter = models.CharField(max_length=15)
    area = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    department = models.CharField(max_length=40)
    wish = models.TextField(max_length=200, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    order_date = models.DateTimeField(default=timezone.now)
    order_status = models.CharField(max_length=15, choices=STATUS, default='В роботі')

    def __str__(self):
        return '{} {} - {}'.format(self.buyer_name, self.buyer_lastname, self.buyer_email)


# куплений продукт
class PurchasedProduct(models.Model):
    session_key = models.CharField(max_length=100)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    image = models.ImageField()
    id_product = models.IntegerField()
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    number = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return '{}'.format(self.title)

    def save(self, *args, **kwargs):
        self.total_price = self.price * self.number
        super(PurchasedProduct, self).save(*args, **kwargs)


# визначення поля загальної ціни продуктів в замовленні
@receiver(post_save, sender=PurchasedProduct)
def add_total_price(instance, **kwargs):
    order = instance.order
    total_price = 0
    purchased_products = PurchasedProduct.objects.filter(order=order)
    for purchased_product in purchased_products:
        total_price += purchased_product.total_price
    order.total_price = total_price
    order.save()
