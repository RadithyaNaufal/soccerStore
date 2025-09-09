from django.shortcuts import render
from .models import Product

def index(request):
    context = {
        "app_name": "Soccer Store",
        "name": "Radithya Naufal Mulia",
        "class": "KKI"
    }
    return render(request, "main.html", context)