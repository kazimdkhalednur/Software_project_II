"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("products.urls")),
    path("orders/", include("orders.urls")),
]

try:
    import debug_toolbar  # noqa: F401

    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
except ImportError:
    pass

try:
    import drf_spectacular  # noqa: F401
    from drf_spectacular import views

    urlpatterns += [
        path("api/schema/", views.SpectacularAPIView.as_view(), name="schema"),
        path(
            "api/schema/swagger-ui/",
            views.SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path(
            "api/schema/redoc/",
            views.SpectacularRedocView.as_view(url_name="schema"),
            name="redoc",
        ),
    ]
except ImportError:
    pass

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
