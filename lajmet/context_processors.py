from .models import Kategoria  # ose emri i modelit tënd për kategoritë

def kategorite_processor(request):
    try:
        kategorite = Kategoria.objects.all()
    except Exception:
        kategorite = []
    
    return {
        'kategorite': kategorite
    }