from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Ship(models.Model):
    id = models.AutoField(primary_key=True)
    shipType = models.CharField("艦種", max_length=240)
    name = models.CharField("型號", max_length=240)
    value = models.FloatField("價值", 
    validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    weight = models.IntegerField("噸位")
    BELONG_CHOICES = (
        ('e', '敵軍'),
        ('a', '我軍'),
    )
    belongsTo = models.CharField(max_length=1, choices=BELONG_CHOICES, default='e')
    def defaultOptionsTemplate():
        return dict({"defaultWeapons":[],})

    options = models.JSONField(blank=True, default=defaultOptionsTemplate)
    def __str__(self):
        return self.name