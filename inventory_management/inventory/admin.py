from django.contrib import admin
from .models import ims_customer,ims_category,ims_brand,ims_supplier,ims_product,ims_purchase,ims_order

# Register your models here.
admin.site.register(ims_customer)
admin.site.register(ims_category)
admin.site.register(ims_brand)
admin.site.register(ims_supplier)
admin.site.register(ims_product)
admin.site.register(ims_purchase)
admin.site.register(ims_order)


