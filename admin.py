from django.contrib import admin
from django.contrib.auth.models import Group,User
from .models import *
# Register your models here.
admin.site.register(categories)
admin.site.register(product)
admin.site.register(product_image)
admin.site.site_header="Aishani"
admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(signup)