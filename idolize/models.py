from django.db import models

class IdolDatabase(models.Model):
    idol_name = models.CharField(max_length=50, unique=True)
    nickname = models.CharField(max_length=50)
    birthdate = models.CharField(max_length=50)
    birthplace = models.CharField(max_length=50)
    zodiac = models.CharField(max_length=50)
    height = models.CharField(max_length=50)
    sns = models.JSONField(default=list)
    
    def __str__(self):
        return self.idol_name