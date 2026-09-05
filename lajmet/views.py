from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Artikull, Kategoria, Koment, Video, Reklama

def faqja_kryesore(request):
    lajmet_list = Artikull.objects.all().order_by('-data_publikimit')
    
    # 3 Lajmet më të fundit fikse për Slider-in
    slider_lajmet = lajmet_list[:3]
    
    kategorite = Kategoria.objects.all()

    # Merr videot nga bazë e të dhënave (p.sh. 4 më të fundit)
    videot = Video.objects.all()[:4]

    reklama = Reklama.objects.filter(is_active=True).last()

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

    # Faqëzimi (Pagination) - 6 lajme për faqe
    paginator = Paginator(lajmet_list, 6) 
    page_number = request.GET.get('page')
    lajmet = paginator.get_page(page_number)

    context = {
        'lajmet': lajmet,
        'slider_lajmet': slider_lajmet,
        'kategorite': kategorite,
        'videot': videot,
        'reklama': reklama,
    }
    return render(request, 'lajmet/index.html', context)

def detajet_e_lajmit(request, pk):
    artikull = get_object_or_404(Artikull, pk=pk)
    
    # Inkremento numrin e shikimeve
    artikull.shikime += 1
    artikull.save(update_fields=['shikime'])
    
    if request.method == 'POST':
        permbajtja = request.POST.get('permbajtja')
        if permbajtja:
            Koment.objects.create(
                artikulli=artikull,
                emri="Anonim",
                permbajtja=permbajtja,
                is_approved=True
            )
            return redirect('detajet_e_lajmit', pk=artikull.pk)

    # Shfaq vetëm komentet e aprovuara
    komentet = artikull.komentet.filter(is_approved=True).order_by('-data_publikimit')
    reklama = Reklama.objects.filter(is_active=True).last()
    
    return render(request, 'lajmet/detajet.html', {
        'artikull': artikull,
        'komentet': komentet,
    })