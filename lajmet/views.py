import xml.etree.ElementTree as ET
import urllib.request
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, F
from django.core.paginator import Paginator
from .models import Artikull, Kategoria, Koment, Video, Reklama

def faqja_kryesore(request):
    for art in Artikull.objects.filter(Q(slug__isnull=True) | Q(slug='')):
        art.save()

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
    reklama = Reklama.objects.filter(is_active=True).last()

    # RSS Feed Fetcher i përmirësuar
    yt_video_id = None
    try:
        feed_url = "https://www.youtube.com/feeds/videos.xml?channel_id=UCgolqCIR2vtRk3L2X_abDTA"
        req = urllib.request.Request(
            feed_url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        xml_data = urllib.request.urlopen(req, timeout=5).read()

        root = ET.fromstring(xml_data)
        
        # Kërkojmë tag-un yt:videoId pavarësisht namespace-it
        for elem in root.iter():
            if elem.tag.endswith('videoId'):
                yt_video_id = elem.text
                break
    except Exception:
        yt_video_id = None

    # Fallback te baza e të dhënave nëse RSS dështon
    if not yt_video_id:
        video_db = Video.objects.last()
        if video_db:
            yt_video_id = video_db.youtube_id

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
        'yt_video_id': yt_video_id,
    }
    return render(request, 'lajmet/index.html', context)