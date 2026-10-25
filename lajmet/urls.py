from django.urls import path
from . import views

urlpatterns = [
    path('', views.faqja_kryesore, name='faqja_kryesore'),
    path('abonohu/', views.faqja_e_abonimit, name='abonohu'),
    path('regjistrohu/', views.regjistrohu, name='regjistrohu'),
    path('hyr/', views.hyrje, name='hyrje'),
    path('dil/', views.dil, name='dil'),
    
    # Rruga për fshirjen e komenteve nga administratori
    path('koment/fshi/<int:koment_id>/', views.fshi_komentin, name='fshi_komentin'),

    # Faqja e lajmeve sipas etiketës
    path('etiketa/<slug:slug>/', views.lajmet_sipas_etiketes, name='lajmet_sipas_etiketes'),
    
    # Rëndësishme: Shtohet KËTU para slug-ut
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
    
    path('<slug:slug>/', views.detajet_e_lajmit, name='detajet_e_lajmit'),
]