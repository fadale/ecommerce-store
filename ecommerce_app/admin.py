from django.contrib import admin

# Register your models here.
from .models import *

from django.contrib.auth.models import User, Group



class ProfileInline(admin.StackedInline):
    model = Register_models
class UserAdmin(admin.ModelAdmin):
    model = User
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User,UserAdmin)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Attribute)
# admin.site.register(Attribute_Value)
admin.site.register(Attribute_product)
admin.site.register(Specification_Product)
admin.site.register(Image_Product)
admin.site.register(Prand)
admin.site.register(Tags)
admin.site.register(Tag_product)
admin.site.register(Slider)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Review)
admin.site.register(Contact)
admin.site.register(FeaturedProducut)
admin.site.register(Category_Side)
admin.site.register(Wishlist)


