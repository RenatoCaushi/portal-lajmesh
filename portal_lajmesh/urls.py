"""
URL configuration for portal_lajmesh project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# 1. Shto këto importe për sitemap-in
from django.contrib.sitemaps.views import sitemap
from lajmet.sitemaps import ArtikullSitemap, KategoriaSitemap

# 2. Përcakto fjalorin e sitemaps
sitemaps = {
    'artikujt': ArtikullSitemap,
    'kategorite': KategoriaSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lajmet.urls')),
    
    # 3. Shto rrugën e sitemap.xml
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)