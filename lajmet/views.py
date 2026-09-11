import json
import urllib.request
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, F
from django.core.paginator import Paginator
from .models import Artikull, Kategoria, Koment, Video, Reklama


def faqja_kryesore(request):
    try:
        for art in Artikull.objects.filter(Q(slug__isnull=True) | Q(slug='')):
            art.save()
    except Exception:
        pass

    lajmet_list = Artikull.objects.all().order_by('-data_publikimit')

    kerko = request.GET.get('kerko')
    if kerko:
        lajmet_list = lajmet_list.filter(
            Q(titulli__icontains=kerko) | Q(permbajtja__icontains=kerko)
        )

    kategoria_id = request.GET.get('kategoria')
    if kategoria_id:
        lajmet_list = lajmet_list.filter(kategoria_id=kategoria_id)

    slider_lajmet = lajmet_list[:3] if not kategoria_id else []
    kategorite = Kategoria.objects.all()
    videot = Video.objects.all()[:4]
    
    try:
        reklama = Reklama.objects.filter(is_active=True).last()
    except Exception:
        reklama = None

    paginator = Paginator(lajmet_list, 6) 
    page_number = request.GET.get('page')
    lajmet = paginator.get_page(page_number)

    context = {
        'lajmet': lajmet,
        'slider_lajmet': slider_lajmet,
        'kategorite': kategorite,
        'videot': videot,
        'reklama': reklama,
        'kategoria_zgjedhur': kategoria_id,
        # VENDOS KËTU ID-TË E VIDEOVE TUA TË YOUTUBE
        'yt_video_1': 'VENDOS_ID_1_KETU', 
        'yt_video_2': 'VENDOS_ID_2_KETU', 
        'yt_video_3': 'VENDOS_ID_3_KETU', 
    }
    return render(request, 'lajmet/index.html', context)


def detajet_e_lajmit(request, slug):
    artikull = get_object_or_404(Artikull, slug=slug)
    
    try:
        Artikull.objects.filter(pk=artikull.pk).update(shikime=F('shikime') + 1)
        artikull.refresh_from_db()
    except Exception:
        pass

    if request.method == 'POST':
        permbajtja = request.POST.get('permbajtja')
        if permbajtja:
            Koment.objects.create(
                artikulli=artikull,
                emri="Anonim",
                permbajtja=permbajtja,
                is_approved=True
            )
            return redirect('detajet_e_lajmit', slug=artikull.slug)

    komentet = artikull.komentet.filter(is_approved=True).order_by('-data_publikimit')
    
    try:
        reklama = Reklama.objects.filter(is_active=True).last()
    except Exception:
        reklama = None
    
    return render(request, 'lajmet/detajet.html', {
        'artikull': artikull,
        'komentet': komentet,
        'reklama': reklama,
    })