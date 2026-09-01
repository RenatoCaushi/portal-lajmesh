from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Artikull, Kategoria, Koment

def faqja_kryesore(request):
    lajmet_list = Artikull.objects.all().order_by('-data_publikimit')
    kategorite = Kategoria.objects.all()

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

    # Faqëzimi (Pagination) - 3 lajme për faqe
    paginator = Paginator(lajmet_list, 3) 
    page_number = request.GET.get('page')
    lajmet = paginator.get_page(page_number)

    context = {
        'lajmet': lajmet,
        'kategorite': kategorite,
    }
    return render(request, 'lajmet/index.html', context)

# Funksioni që mungonte:
def detajet_e_lajmit(request, pk):
    artikulli = get_object_or_404(Artikull, pk=pk)
    
    # Trajtimi i dërgimit të komenteve
    if request.method == 'POST':
        emri = request.POST.get('emri')
        teksti = request.POST.get('teksti')
        if emri and teksti:
            Koment.objects.create(artikulli=artikulli, emri=emri, teksti=teksti)
            return redirect('detajet_e_lajmit', pk=artikulli.pk)

    return render(request, 'lajmet/detajet.html', {'artikull': artikulli})