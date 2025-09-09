from django.shortcuts import render
from .models import Product

def index(request):
    context = {
        "app_name": "Soccer Store",
        "name": "Radithya Naufal Mulia",
        "npm": "2406365225",
        "class": "KKI",
        "products": Product.objects.all()
    }
    return render(request, "main.html", context)