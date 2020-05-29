from django.contrib import admin

from .models import Author, Address, Book, Publication, Category, Order, OrderItem, Client

admin.site.register(Author)
admin.site.register(Address)
admin.site.register(Book)
admin.site.register(Publication)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Client)
