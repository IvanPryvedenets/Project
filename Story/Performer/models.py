from django.db import models


class Category(models.Model):
    field = models.CharField(max_length=50)

    def __str__(self):
        return 'Category: {}'.format(self.field)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField()
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    old_price = models.DecimalField(max_digits=3, decimal_places=2)
    price = models.DecimalField(max_digits=3, decimal_places=2)
    slug = models.CharField(max_length=100)
    stock = models.CharField(max_length=25, default='В наявності')

    def get_absolute_url(self):
        return
