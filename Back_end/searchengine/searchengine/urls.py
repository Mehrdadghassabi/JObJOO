from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.sitemaps import views
from django.views.decorators.cache import cache_page
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# from management.views import *
from searchengine import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Recruiment view API",
        default_version='v1',
        description="The first API of recruiment controller",
        contact=openapi.Contact(email="navid.shagho003@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.IsAdminUser,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include(('authentication.urls', 'authentication'))),
    path('api/', include(('api.urls', 'api'))),
    path('api-auth/', include('rest_framework.urls')),
    url(r'^doc(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^doc1/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^doc2/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('robots.txt', Robots.as_view(), name='robots.txt'),
    # path('contact/', Contact.as_view(), name='contact'),
    # path('about/', About.as_view(), name='about'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)