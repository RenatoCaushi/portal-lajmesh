from .models import Kategoria

def kategorite_processor(request):
    return {
        'kategorite': Kategoria.objects.all()
    }