from django.contrib import admin
from .models import Product,Payment,Contact,Coupon

# Register your models here.
admin.site.register(Product)
admin.site.register(Payment)
admin.site.register(Coupon)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
