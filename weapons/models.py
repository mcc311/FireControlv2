from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
class Weapon(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("型號", max_length=240)
    damage = models.FloatField("毀傷值", default=.5,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    range = models.FloatField("射程", validators=[MinValueValidator(0.0)], default=300)
    BELONG_CHOICES = (
        ('e', '敵軍'),
        ('a', '我軍'),
    )
    belongsTo = models.CharField(max_length=1, choices=BELONG_CHOICES, default='e')
    cost = models.IntegerField(default=100)
    def __str__(self):
        return self.name

