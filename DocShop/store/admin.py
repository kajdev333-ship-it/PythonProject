from django.contrib import admin

from store.models import product, Order,Order_bijoux, Order_cosmetique, Order_electronique,  Cart, Electronique, Cart_electronique, Cosmetique, Bijoux, Cart_cosmetique, Cart_bijoux, Subscriber

# Register your models here.
admin.site.register(product)
admin.site.register(Electronique)
admin.site.register(Cosmetique)
admin.site.register(Bijoux)
admin.site.register(Order)
admin.site.register(Order_bijoux)
admin.site.register(Order_cosmetique)
admin.site.register(Order_electronique)
admin.site.register(Cart)
admin.site.register(Cart_electronique)
admin.site.register(Cart_cosmetique)
admin.site.register(Cart_bijoux)
admin.site.register(Subscriber)
