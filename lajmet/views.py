from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.urls import reverse
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
    ka_akses = True
    if artikull.eshte_premium:
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


def regjistrohu(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('faqja_kryesore')
    else:
        form = UserCreationForm()
    
    kategorite = Kategoria.objects.all()
    context = {
        'form': form,
        'kategorite': kategorite,
    }
    return render(request, 'lajmet/regjistrohu.html', context)


def hyrje(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('faqja_kryesore')
    else:
        form = AuthenticationForm()
    
    kategorite = Kategoria.objects.all()
    context = {
        'form': form,
        'kategorite': kategorite,
    }
    return render(request, 'lajmet/hyrje.html', context)


def dil(request):
    logout(request)
    return redirect('faqja_kryesore')


@staff_member_required
def fshi_komentin(request, koment_id):
    koment = get_object_or_404(Koment, id=koment_id)
    artikull_slug = koment.artikulli.slug
    koment.delete()
    return redirect('detajet_e_lajmit', slug=artikull_slug)


def sitemap_xml(request):
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    # 1. Faqja kryesore
    xml.append('  <url>')
    xml.append(f'    <loc>{request.build_absolute_uri(reverse("faqja_kryesore"))}</loc>')
    xml.append('    <changefreq>daily</changefreq>')
    xml.append('    <priority>1.0</priority>')
    xml.append('  </url>')
    
    # 2. Faqet statike kryesore
    faqet_statike = ['abonohu', 'regjistrohu', 'hyr']
    for faqe in faqet_statike:
        try:
            url = request.build_absolute_uri(reverse(faqe))
            xml.append('  <url>')
            xml.append(f'    <loc>{url}</loc>')
            xml.append('    <changefreq>monthly</changefreq>')
            xml.append('    <priority>0.7</priority>')
            xml.append('  </url>')
        except Exception:
            pass

    # 3. Artikujt duke përdorur slug-un ekzistues
    try:
        artikujt = Artikull.objects.all().order_by('-data_publikimit')[:200]
        for art in artikujt:
            if art.slug:
                url = request.build_absolute_uri(reverse('detajet_e_lajmit', kwargs={'slug': art.slug}))
                xml.append('  <url>')
                xml.append(f'    <loc>{url}</loc>')
                xml.append('    <changefreq>never</changefreq>')
                xml.append('    <priority>0.6</priority>')
                xml.append('  </url>')
    except Exception:
        pass
            
    xml.append('</urlset>')
    
    return HttpResponse("\n".join(xml), content_type="application/xml")