from django.contrib import admin
from .models import Customer,Invoice,InvoiceItem
# Register your models here.
admin.site.register(Customer)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)
