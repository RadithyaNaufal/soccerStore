from django.forms import ModelForm
from django import forms
from main.models import News

class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = ["name","price","description","category","thumbnail","is_featured"]