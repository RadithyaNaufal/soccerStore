import uuid
from django.db import models
from django.contrib.auth.models import User

class News(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
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
    news_views = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.name

    @property
    def is_news_hot(self):
        return self.news_views > 20

    def increment_views(self):
        self.news_views += 1
        self.save()