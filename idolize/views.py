from django.shortcuts import render, get_list_or_404
from django.views.generic import TemplateView, FormView, DetailView
from django.forms import modelform_factory
from django.core.exceptions import *
from django.db.models import Q
from django.http import JsonResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, mixins

from .forms import IdolSearchForm
from .models import IdolDatabase
from .serializers import IdolSerializer

class IdolSearch(FormView):
    template_name = "idolize/index.html"
    form_class = IdolSearchForm

    def form_valid(self, form):
        zodiac = form.cleaned_data.get("zodiac")
        height = form.cleaned_data.get("height")
        birthplace = form.cleaned_data.get("birthplace")

        result = None
        fake_result = None

        best_match = IdolDatabase.objects.filter(
            Q(zodiac__iexact=zodiac) & 
            Q(height__iexact=height) & 
            Q(birthplace__icontains=birthplace)
        )

        if best_match.exists():
            result = best_match
        else:
            medium_match = IdolDatabase.objects.filter(
                (Q(zodiac__iexact=zodiac) & Q(height__iexact=height)) |
                (Q(zodiac__iexact=zodiac) & Q(birthplace__icontains=birthplace)) |
                (Q(height__iexact=height) & Q(birthplace__icontains=birthplace))
            )
            if medium_match.exists():
                result = medium_match
            else:
                ok_match = IdolDatabase.objects.filter(
                    Q(zodiac__iexact=zodiac) | 
                    Q(height__iexact=height) | 
                    Q(birthplace__icontains=birthplace)
                )
                result = ok_match

        if not result.exists():
            fake_result = True
            result = [IdolDatabase.objects.get(idol_name="Matsumoto Karen")]

        return render(self.request, "idolize/result.html", {"matching_idols": result, "fake_result": fake_result})
    
class IdolProfileView(DetailView):

    template_name = "idolize/profileview.html"
    model = IdolDatabase
    context_object_name = "idol"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["idol_name"] = self.object.idol_name

        sns_links = []
        for platform, link in self.object.sns.items():
            sns_links.append({"platform": platform, "link": link})

        context["sns_links"] = sns_links
        return context
    
class IdolList(generics.ListAPIView):
    queryset = IdolDatabase.objects.all()
    serializer_class = IdolSerializer

class IdolDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = IdolDatabase.objects.all()
    serializer_class = IdolSerializer