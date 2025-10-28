from django.shortcuts import render, redirect, get_object_or_404
from main.forms import NewsForm
from main.models import News
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import datetime
import json
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")
    if filter_type == "all":
        news_list = News.objects.all()
    else:
        news_list = News.objects.filter(user=request.user)
    context = {
        'app_name': 'Soccer Store',
        'npm': '2406365225',
        'name': request.user.username,
        'class': 'KKI',
        'news_list': news_list,
        'last_login': request.COOKIES.get('last_login', 'Never'),
    }
    return render(request, "main.html", context)

@login_required(login_url='/login')
def show_category(request, category):
    news_list = News.objects.filter(category=category)
    context = {
        'app_name': 'Soccer Store',
        'npm': '2406365225',
        'name': request.user.username,
        'class': 'KKI',
        'news_list': news_list,
        'last_login': request.COOKIES.get('last_login', 'Never'),
    }
    return render(request, "main.html", context)

@login_required(login_url='/login')
def create_news(request):
    form = NewsForm(request.POST or None)
    if form.is_valid() and request.method == 'POST':
        news_entry = form.save(commit=False)
        news_entry.user = request.user
        news_entry.save()
        return redirect('main:show_main')
    context = {'form': form}
    return render(request, "create_news.html", context)

@login_required(login_url='/login')
def show_news(request, id):
    news = get_object_or_404(News, pk=id)
    news.increment_views()
    context = {'news': news}
    return render(request, "news_detail.html", context)

def show_xml(request):
    news_list = News.objects.all()
    xml_data = serializers.serialize("xml", news_list)
    return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    news_list = News.objects.all()
    data = [
        {
            'id': str(news.id),
            'name': news.name,
            'price': news.price,
            'description': news.description,
            'category': news.category,
            'thumbnail': news.thumbnail,
            'news_views': news.news_views,
            'created_at': news.created_at.isoformat() if news.created_at else None,
            'is_featured': news.is_featured,
            'user_id': news.user_id,
        }
        for news in news_list
    ]
    return JsonResponse(data, safe=False)

def show_xml_by_id(request, news_id):
    try:
        news_item = News.objects.filter(pk=news_id)
        xml_data = serializers.serialize("xml", news_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except News.DoesNotExist:
        return HttpResponse(status=404)

def show_json_by_id(request, news_id):
    try:
        news = News.objects.select_related('user').get(pk=news_id)
        data = {
            'id': str(news.id),
            'name': news.name,
            'price': news.price,
            'description': news.description,
            'category': news.category,
            'thumbnail': news.thumbnail,
            'news_views': news.news_views,
            'created_at': news.created_at.isoformat() if news.created_at else None,
            'is_featured': news.is_featured,
            'user_id': news.user_id,
            'user_username': news.user.username if news.user_id else None,
        }
        return JsonResponse(data)
    except News.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)

def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form': form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def edit_news(request, id):
    news = get_object_or_404(News, pk=id)
    form = NewsForm(request.POST or None, instance=news)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')
    context = {'form': form}
    return render(request, "edit_news.html", context)

def delete_news(request, id):
    news = get_object_or_404(News, pk=id)
    if news.user == request.user or request.user.is_superuser:
        news.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

@login_required(login_url='/login')
def get_news_json(request):
    filter_type = request.GET.get('filter')
    category_type = request.GET.get('category')

    if filter_type == 'my':
        news_list = News.objects.filter(user=request.user)
    else:
        news_list = News.objects.all()

    if category_type:
        news_list = news_list.filter(category=category_type)
    
    news_list = news_list.order_by('-created_at')

    data = []
    for news in news_list:
        data.append({
            "pk": news.pk,
            "user_id": news.user.id,
            "user_username": news.user.username,
            "name": news.name,
            "price": news.price,
            "description": news.description,
            "thumbnail": news.thumbnail,
            "category": news.category,
            "created_at": news.created_at.strftime("%d %B %Y"),
            "news_views": news.news_views,
        })

    return JsonResponse(data, safe=False)

@csrf_exempt
@login_required(login_url='/login')
def create_news_ajax(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        thumbnail = request.POST.get("thumbnail")
        category = request.POST.get("category")
        is_featured = request.POST.get("is_featured") == "true"
        new_news = News.objects.create(
            user=request.user,
            name=name,
            price=int(price),
            description=description,
            thumbnail=thumbnail,
            category=category,
            is_featured=is_featured,
        )
        return JsonResponse({"status": "success", "id": str(new_news.id)})
    return JsonResponse({"status": "error"}, status=400)

@csrf_exempt
@login_required(login_url='/login')
def delete_news_ajax(request, id):
    if request.method == 'POST':
        news = get_object_or_404(News, pk=id, user=request.user)
        news.delete()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)

@csrf_exempt
@login_required(login_url='/login')
def edit_news_ajax(request, id):
    if request.method == 'POST':
        news = get_object_or_404(News, pk=id, user=request.user)
        news.name = request.POST.get("name")
        news.price = int(request.POST.get("price"))
        news.description = request.POST.get("description")
        news.thumbnail = request.POST.get("thumbnail")
        news.category = request.POST.get("category")
        news.is_featured = request.POST.get("is_featured") == "true"
        news.save()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)

@csrf_exempt
def register_ajax(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"status": "success", "message": "Account created successfully!"}, status=201)
        else:
            return JsonResponse({"status": "error", "errors": form.errors}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

@csrf_exempt
def login_ajax(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = JsonResponse({"status": "success", "message": "Login successful!"})
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            return JsonResponse({"status": "error", "message": "Invalid username or password."}, status=401)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

def logout_ajax(request):
    logout(request)
    return JsonResponse({"status": "success", "message": "You have been logged out."})