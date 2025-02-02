from django.forms import ModelForm
from idolize.models import IdolDatabase

class IdolSearchForm(ModelForm):
    class Meta:
        model = IdolDatabase
        fields = ["zodiac", "height", "birthplace"]

    def clean_height(self):
        height = self.cleaned_data.get("height")
        valid_height = height.replace("cm","").strip()
        return valid_height