from rest_framework import serializers
from idolize.models import IdolDatabase

class IdolSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdolDatabase
        fields = ["idol_name", "nickname", "birthdate", "birthplace", "zodiac", "height", "sns"]