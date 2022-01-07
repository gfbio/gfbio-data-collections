from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
                  path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
                  # path("",include("gfbio_collections.frontend.urls", namespace="frontend")),
                  path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
                  # Django Admin, use {% url 'admin:index' %}
                  path(settings.ADMIN_URL, admin.site.urls),
                  # User management
                  path("users/", include("gfbio_collections.users.urls", namespace="users")),
                  path("accounts/", include("allauth.urls")),
                  # Collection management
                  path("api/", include("gfbio_collections.collection.urls", namespace="api")),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# API URLS
urlpatterns += [
    # API base url
    # path("api/", include("config.api_router")),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
]

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='jwt_obtain_token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='jwt_token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='jwt_token_verify'),
]
# for HTML documentation (swagger)

schema_url_patterns = [
    path('api/', include('gfbio_collections.collection.urls')),
]

urlpatterns += [
    # ...
    # Use the `get_schema_view()` helper to add a `SchemaView` to project URLs.
    #   * `title` and `description` parameters are passed to `SchemaGenerator`.
    #   * Provide view name for use with `reverse()`.
    path('openapi', get_schema_view(
        title="Collection Service",
        description="Service for collection of Data Identifiers",
        version="0.0.1",
        patterns=schema_url_patterns,
        permission_classes=[permissions.AllowAny]
    ), name='openapi-schema'),
    # ...
]

urlpatterns += [
    # ...
    # Route TemplateView to serve Swagger UI template.
    #   * Provide `extra_context` with view name of `SchemaView`.
    path('swagger/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'},
    ), name='swagger-ui'),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
