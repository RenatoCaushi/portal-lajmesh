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
from django.http import HttpResponse

from django.contrib.sitemaps.views import sitemap
from lajmet.sitemaps import ArtikullSitemap, KategoriaSitemap

sitemaps = {
    'artikujt': ArtikullSitemap,
    'kategorite': KategoriaSitemap,
}


def robots_txt(request):
    """robots.txt pa skedar template: nuk mund të japë gabim 500 nëse mungon një skedar."""
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /ckeditor5/",
        "Allow: /",
        "",
        "Sitemap: https://%s/sitemap.xml" % request.get_host(),
    ]
    return HttpResponse(
        "\n".join(lines) + "\n", content_type="text/plain; charset=utf-8"
    )


urlpatterns = [
    # Robots.txt dhe sitemap vihen para 'lajmet.urls', që asnjë rrugë tjetër të mos i kapë
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    path('admin/', admin.site.urls),
    path('', include('lajmet.urls')),

    # Rruga e re për CKEditor-in (E detyrueshme që të mos japi error 500)
    path("ckeditor5/", include('django_ckeditor_5.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)