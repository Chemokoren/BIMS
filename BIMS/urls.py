"""
BIMS URL Configuration

"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include([
                    path('', include('authentication.apis.urls')),
                    path('', include('book_inventory_app.apis.urls')),
            ]))
]
