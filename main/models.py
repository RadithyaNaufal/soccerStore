import uuid
from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('basket', 'Basket'),
        ('futsal', 'Futsal'),
        ('sepatu', 'Sepatu'),
        ('tas', 'Tas'),
        ('jersey', 'Jersey'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name