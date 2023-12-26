from django.contrib import admin

# Register your models here.
from .models import AdminAccount,Lost_Item

admin.site.register(AdminAccount)
admin.site.register(Lost_Item)