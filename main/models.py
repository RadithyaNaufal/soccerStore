import uuid
from django.db import models

class News(models.Model):
    CATEGORY_CHOICES = [
        ('basketball', 'BasketBall'),
        ('soccerBall', 'SoccerBall'),
        ('shoes', 'Shoes'),
        ('backpack', 'Backpack'),
        ('jersey', 'Jersey'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name