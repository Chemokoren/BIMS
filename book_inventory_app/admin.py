from django.contrib import admin
from .models import Stock
from simple_history.admin import SimpleHistoryAdmin
# Register your models here.
admin.site.register(Stock,SimpleHistoryAdmin)