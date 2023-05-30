"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/schema/',SpectacularAPIView.as_view(), name = 'api-schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name = 'api-docs',
        ),
    path('api/user/',include('user.urls')),
    path('api/', include('project.urls')),
]
#    path('api/recipe/', include('recipe.urls')),

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root = settings.MEDIA_ROOT,
    )

""" Here we are mimicking the behaviour we expect when we use development server"""
""" Django dev server by default does not serve these files for us, need to add this """
""" in order for it to serve media files """

""" Have settings.DEBUG, so only do this in debug mode, as when we're running in prod """
"""dont want to be serving media files from dev server """