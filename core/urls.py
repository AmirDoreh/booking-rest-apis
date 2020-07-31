from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(openapi.Info(title="Booking API", default_version="v1",),)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cleaners/", include("cleaners.urls")),
    path("books/", include("books.urls")),
    path(
        "doc/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "doc/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
