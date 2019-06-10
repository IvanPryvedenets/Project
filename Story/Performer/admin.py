from django.contrib import admin
from .models import *


class AdminCategory(admin.ModelAdmin):

    model = Category


admin.site.register(Category)
