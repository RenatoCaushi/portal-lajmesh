import json
import urllib.request
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, F
from django.core.paginator import Paginator
from .models import Artikull, Kategoria, Koment, Video, Reklama

# Çelësi yt zyrtar i YouTube API v3
YOUTUBE_API_KEY = 'AIzaSyBVJo36lphLUy9Dmv2EdISLpoLTvrfCcIw'
YOUTUBE_CHANNEL_ID = 'UCgolqCIR2vtRk3L2X_abDTA'


def faqja_kryesore(request):
    # Plotëson automatikisht slug-un për çdo artikull bosh
    try:
        for art in Artikull.objects.filter(Q(slug__isnull=True) | Q(slug='')):
            art.save()
    except Exception:
        pass

    lajmet_list = Artikull.objects.all().order_by('-data_publikimit')

    # Kërkimi me fjalë kyçe
    kerko = request.GET.get('kerko')
    if kerko:
        lajmet_list = lajmet_list.filter(
            Q(titulli__icontains=kerko) | Q(permbajtja__icontains=kerko)
        )

    # Filtrimi sipas kategorisë
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

    # --- MARRJA E VIDEOS PËRMES YOUTUBE DATA API V3 ---
    yt_video_id = None
    try:
        api_url = (
            f"https://www.googleapis.com/youtube/v3/search"
            f"?key={YOUTUBE_API_KEY}"
            f"&channelId={YOUTUBE_CHANNEL_ID}"
            f"&part=snippet,id"
            f"&order=date"
            f"&maxResults=1"
            f"&type=video"
        )
        req = urllib.request.Request(
            api_url, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode('utf-8'))
            items = data.get('items', [])
            if items:
                yt_video_id = items[0]['id']['videoId']
    except Exception:
        yt_video_id = None

    # Fallback i sigurt nga DB nëse API dështon ose mbarojnë kuotat
    if not yt_video_id:
        try:
            video_db = Video.objects.last()
            if video_db:
                yt_video_id = getattr(video_db, 'youtube_id', None) or getattr(video_db, 'video_id', None)
        except Exception:
            yt_video_id = None

    # Faqëzimi (Pagination)
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