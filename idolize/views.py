from django.shortcuts import render
from django.views.generic import FormView, DetailView
from django.core.exceptions import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from rest_framework import generics 

from .forms import IdolSearchForm
from .models import IdolDatabase
from .serializers import IdolSerializer

class IdolSearch(FormView):
    template_name = "idolize/index.html"
    form_class = IdolSearchForm

    def form_valid(self, form):
        self.zodiac = form.cleaned_data.get("zodiac")
        self.height = form.cleaned_data.get("height")
        self.birthplace = form.cleaned_data.get("birthplace")

        matching_idols, fake_result = self.determine_match()

        #handling of the True or False check of fake_result is handled in the result.html to make it easier to show different content based on the result
        return render(self.request, "idolize/result.html", {
            "matching_idols": matching_idols, 
            "fake_result": fake_result
        })

    def determine_match(self):
        best_match = IdolDatabase.objects.filter(
            Q(zodiac__iexact=self.zodiac) & 
            Q(height__iexact=self.height) & 
            Q(birthplace__icontains=self.birthplace)
        )
        if best_match.exists():
            return best_match, False
    
        medium_match = IdolDatabase.objects.filter(
            (Q(zodiac__iexact=self.zodiac) & Q(height__iexact=self.height)) |
            (Q(zodiac__iexact=self.zodiac) & Q(birthplace__icontains=self.birthplace)) |
            (Q(height__iexact=self.height) & Q(birthplace__icontains=self.birthplace))
        )
        if medium_match.exists():
            return medium_match, False
        
        ok_match = IdolDatabase.objects.filter(
            Q(zodiac__iexact=self.zodiac) | 
            Q(height__iexact=self.height) | 
            Q(birthplace__icontains=self.birthplace)
        )
        if ok_match.exists():
            return ok_match,False
                
        #not showing any result in case there are no matching parameters is boring, so we always show a predetermined result as long as there is input
        return [IdolDatabase.objects.get(idol_name="Matsumoto Karen")], True
    
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