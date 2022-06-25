from django.core.paginator import Paginator
from django.shortcuts import render
from .models import *
from .forms import *

def home(requset):
    form = FindForm()
    return render(requset, 'app/home.html', context={'form': form})

def list(requset):
    form = FindForm()

    city = requset.GET.get('city')
    language = requset.GET.get('language')
    context = {'city': city, 'language': language, 'form' : form}

    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language

        qs = Vacancy.objects.filter(**_filter)
        paginator = Paginator(qs, 10)

        page_number = requset.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj


    return render(requset, 'app/list.html', context)