from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Artikull, Kategoria, Koment, Reklama


def faqja_kryesore(request):
    # Rregullon artikujt pa slug nese ka
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
        'reklama': reklama,
        'kategoria_zgjedhur': kategoria_id,
    }
    return render(request, 'lajmet/index.html', context)


def detajet_e_lajmit(request, slug):
    artikull = get_object_or_404(Artikull, slug=slug)
    
    # HEQUR: Rritja e numrit të shikimeve (pasi fusha shikime u fshi)

    # Trajtimi i dërgimit të formularit të komenteve
    if request.method == 'POST':
        emri = request.POST.get('emri', '').strip()
        permbajtja = request.POST.get('permbajtja', '').strip()

        if permbajtja:
            Koment.objects.create(
                artikulli=artikull,
                emri=emri if emri else 'Anonim',
                permbajtja=permbajtja,
                is_approved=True  # Ruan komentin direkt si të miratuar
            )
            return redirect('detajet_e_lajmit', slug=artikull.slug)

    kategorite = Kategoria.objects.all()
    
    try:
        reklama = Reklama.objects.filter(is_active=True).last()
    except Exception:
        reklama = None

    # Kontrolli për Paywall:
    # Për momentin le të përcaktojmë se një përdorues ka akses nëse është i loguar (superuser ose staff),
    # ose mund ta përshtasim sipas dëshirës. Për testim, përdoruesit e loguar shohin gjithçka.
    ka_akses = True
    if artikull.eshte_premium:
        # Nëse artikulli është premium, kontrollojmë nëse përdoruesi është i loguar
        # (Më vonë mund ta lidhim me një model Abonimi)
        if not request.user.is_authenticated:
            ka_akses = False

    context = {
        'artikull': artikull,
        'kategorite': kategorite,
        'reklama': reklama,
        'ka_akses': ka_akses,
    }
    return render(request, 'lajmet/detajet.html', context)

def faqja_e_abonimit(request):
    kategorite = Kategoria.objects.all()
    context = {
        'kategorite': kategorite,
    }
    return render(request, 'lajmet/abonohu.html', context)