import xml.etree.ElementTree as ET
import urllib.request
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, F
from django.core.paginator import Paginator
from .models import Artikull, Kategoria, Koment, Video, Reklama

def faqja_kryesore(request):
    # Plotëson automatikisht slug-un për çdo artikull që ka mbetur bosh në bazën e të dhënave
    for art in Artikull.objects.filter(Q(slug__isnull=True) | Q(slug='')):
        art.save()

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

    # NËSE është zgjedhur kategori, mos shfaq slider të pavarur që përzien lajmet
    slider_lajmet = lajmet_list[:3] if not kategoria_id else []

    kategorite = Kategoria.objects.all()
    videot = Video.objects.all()[:4]
    reklama = Reklama.objects.filter(is_active=True).last()

    # Marrja automatike e videos më të fundit nga YouTube RSS Feed
    yt_video_id = None
    try:
        feed_url = "https://www.youtube.com/feeds/videos.xml?channel_id=UCgolqCIR2vtRk3L2X_abDTA"
        req = urllib.request.Request(
            feed_url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        xml_data = urllib.request.urlopen(req, timeout=5).read()

        root = ET.fromstring(xml_data)
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
    
    Artikull.objects.filter(pk=artikull.pk).update(shikime=F('shikime') + 1)
    artikull.refresh_from_db()

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
    reklama = Reklama.objects.filter(is_active=True).last()
    
    return render(request, 'lajmet/detajet.html', {
        'artikull': artikull,
        'komentet': komentet,
        'reklama': reklama,
    })