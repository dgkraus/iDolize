from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import TemplateView
from django.core.exceptions import *
from django.db.models import Q

from .forms import IdolSearchForm
from .models import IdolDatabase

def idol_search(request):

    if request.method == "POST":

        form = IdolSearchForm(request.POST)

        if form.is_valid():
            cleaned_form = form.cleaned_data
            zodiac = cleaned_form.get("your_zodiac").strip()
            height = cleaned_form.get("your_height").replace("cm","").strip()
            birthplace = cleaned_form.get("your_birthplace").strip()
        
        fake_result = None

        best_match = IdolDatabase.objects.filter(
            Q(zodiac__iexact=zodiac) & 
            Q(height__iexact=height) & 
            Q(birthplace__icontains=birthplace)
        )
        
        if len(best_match) != 0:
            result = best_match
        
        else:
            medium_match = IdolDatabase.objects.filter(
                (Q(zodiac__iexact=zodiac) & Q(height__iexact=height)) |
                (Q(zodiac__iexact=zodiac) & Q(birthplace__icontains=birthplace)) |
                (Q(height__iexact=height) & Q(birthplace__icontains=birthplace))
            )
            if len(best_match) == 0 and len(medium_match) != 0:
                result = medium_match
            
            else:
                ok_match = results = IdolDatabase.objects.filter(
                    Q(zodiac__iexact=zodiac) | 
                    Q(height__iexact=height) | 
                    Q(birthplace__icontains=birthplace)
                )
                result = ok_match
        
        if len(result) == 0:
            fake_result = True
            result = [IdolDatabase.objects.get(idol_name="Matsumoto Karen")]


        return render(request, "idolize/result.html", {"matching_idols": result, "fake_result": fake_result})

    else:
        form = IdolSearchForm()

    return render(request, "idolize/index.html", {"form": form})