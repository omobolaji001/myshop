from django.contrib import admin
from .models import Category, Product
from parler.admin import TranslatableAdmin


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    """ Registers the categoryy model to the Admin page """
    list_display = ['name', 'slug']

    def get_prepopulated_fields(self, request, obj=None):
        """ Returns the slug of the name field """
        return {
            'slug': ('name',)
        }


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    """ Registers the product model to the Admin page """
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']

    def get_prepopulated_fields(self, request, obj=None):
        """ Returns the slug of the name field """
        return {
            'slug': ('name',)
        }
