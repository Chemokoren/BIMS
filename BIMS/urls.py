"""
BIMS URL Configuration

"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view
from rest_framework import permissions

schema_view = swagger_get_schema_view(
    openapi.Info(
        title="BIMS API",
        default_version='1.0.0',
        description=f"API documentation for { settings.SITE_NAME }"
    ),
    permission_classes=(permissions.AllowAny,),
    public=False,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include([
                    path('', include('authentication.apis.urls')),
                    path('', include('book_inventory_app.apis.urls')),
                    path('swagger/schema/', schema_view.with_ui('swagger', cache_timeout=0), name="swagger-schema"),
            ]))
]
