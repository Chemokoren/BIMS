"""
BIMS URL Configuration

"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include([
                    path('', include('authentication.apis.urls')),
                    path('', include('book_inventory_app.apis.urls')),
                    path("schema/", SpectacularAPIView.as_view(), name="schema"),
                    path(
                        "docs/",
                        SpectacularSwaggerView.as_view(
                            template_name="swagger-ui.html", url_name="schema"
                        ),
                        name="swagger-ui",
                    ),
            ]))
]
