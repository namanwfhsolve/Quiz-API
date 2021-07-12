"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Quiz API",
        default_version="v1",
        description="A simple Quiz API",
        contact=openapi.Contact(email="namantam1@gmail.com"),
        license=openapi.License(
            name="MIT License",
            url="https://github.com/namanwfhsolve/Quiz-API/blob/main/LICENSE",
        ),
    ),
    public=True,
    # authentication_classes=(authentication.SessionAuthentication, JWTAuthentication),
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # ADMIN
    path("admin/", admin.site.urls),
    # AUTHENTICATION API
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # QUIZ APP
    path("quiz/", include("quiz.urls")),
    # APIS Docs
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if getattr(settings, "ENABLE_DEBUG_TOOLBAR", False):
    from debug_toolbar import urls as debug_urls

    urlpatterns += [path("__debug__/", include(debug_urls))]
