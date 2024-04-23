from django.contrib import admin
from .models import Orders
from .forms import OrderForm


@admin.register(Orders)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'status']
    ordering = ['-id']
    search_field = ['title']
    list_per_page = 20

