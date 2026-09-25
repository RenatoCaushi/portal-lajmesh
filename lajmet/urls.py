from django.urls import path
from . import views

urlpatterns = [
    path('', views.faqja_kryesore, name='faqja_kryesore'),
    path('abonohu/', views.faqja_e_abonimit, name='abonohu'),
    path('regjistrohu/', views.regjistrohu, name='regjistrohu'),
    path('hyr/', views.hyrje, name='hyrje'),
    path('dil/', views.dil, name='dil'),
    
    # Rëndësishme: Shtohet KËTU para slug-ut
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
    
    path('<slug:slug>/', views.detajet_e_lajmit, name='detajet_e_lajmit'),
]