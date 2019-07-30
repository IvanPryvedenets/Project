from django.contrib import admin
from .models import *


class AdminCategory(admin.ModelAdmin):

    model = Category


admin.site.register(Category)


class AdminProduct(admin.ModelAdmin):

    list_display = ('id', 'category', 'title', 'description', 'brand', 'price', 'old_price', 'stock',)

    search_fields = ['id', 'category__field', 'brand']

    fieldsets = (
        ('Product information', {
            'fields': ('category', 'image', 'title', 'description', 'brand', 'old_price', 'price', 'weight')
        }),

        ('System information', {
            'fields': ('slug', 'stock')
        })
    )


admin.site.register(Product, AdminProduct)


class AdminComment(admin.ModelAdmin):

    list_display = ('id', 'user_name', 'user_email', 'message', 'date_pub')


admin.site.register(Comment, AdminComment)


class AdminBasket(admin.ModelAdmin):

    list_display = ('product', 'id_product', 'title', 'price', 'number', 'total_price')


admin.site.register(Basket, AdminBasket)


class AdminPurchasedProduct(admin.TabularInline):
    model = PurchasedProduct

    exclude = ['session_key', 'image']

    readonly_fields = ['title', 'id_product', 'price', 'number', 'total_price']

    extra = 0


class AdminOrder(admin.ModelAdmin):

    search_fields = ('buyer_name', 'buyer_lastname', 'buyer_email')

    list_display = ('buyer_name', 'buyer_lastname', 'user_status', 'buyer_email', 'buyer_tel', 'area', 'city', 'department','total_price', 'order_date', 'order_status')

    fieldsets = (
        ('Buyer information', {
            'fields': ('buyer_name', 'buyer_lastname', 'user_status', 'buyer_tel', 'buyer_email')
        }),

        ('Pay way', {
            'fields': ('pay_way',)
        }),

        ('Delivery information', {
            'fields': ('transporter', 'area', 'city', 'department')
        }),

        ('Other information', {
            'fields': ('wish', 'total_price', 'order_date', 'order_status')
        })
    )

    inlines = [AdminPurchasedProduct]


admin.site.register(Order, AdminOrder)

