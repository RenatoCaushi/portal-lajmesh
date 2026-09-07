from django.urls import path
from . import views

urlpatterns = [
    path('', views.faqja_kryesore, name='faqja_kryesore'),
    path('lajmi/<slug:slug>/', views.detajet_e_lajmit, name='detajet_e_lajmit'),
]