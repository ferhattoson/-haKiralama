from django.db import models
from django.contrib.auth.models import User

class İHA(models.Model):
    id = models.AutoField(primary_key=True) 
    ihaAd = models.CharField(max_length=255)
    ihaMarka = models.CharField(max_length=255)
    ihaModel = models.CharField(max_length=255)
    ihaAgirlik = models.DecimalField(max_digits=10, decimal_places=2)
  
class Kiralanan(models.Model):
    id = models.AutoField(primary_key=True) 
    kullanici = models.ForeignKey(User, on_delete=models.CASCADE)
    iha = models.ForeignKey(İHA, on_delete=models.CASCADE)
    baslangicTarihi = models.DateField()
    bitisTarihi = models.DateField()
