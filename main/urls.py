from django.urls import path
from main.views import show_main, create_news, show_news, show_xml, show_json, show_xml_by_id, show_json_by_id, register, login_user, logout_user, edit_news, delete_news, show_category, get_news_json, create_news_ajax, edit_news_ajax, delete_news_ajax, register_ajax, login_ajax, logout_ajax

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-news/', create_news, name='create_news'),
    path('news/<uuid:id>/', show_news, name='show_news'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<uuid:news_id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<uuid:news_id>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('news/<uuid:id>/edit', edit_news, name='edit_news'),
    path('news/<uuid:id>/delete', delete_news, name='delete_news'),
    path('category/<str:category>/', show_category, name='show_category'),
    path('get-news-json/', get_news_json, name='get_news_json'),
    path('create-news-ajax/', create_news_ajax, name='create_news_ajax'),
    path('edit-news-ajax/<uuid:id>/', edit_news_ajax, name='edit_news_ajax'),
    path('delete-news-ajax/<uuid:id>/', delete_news_ajax, name='delete_news_ajax'),
    path('register-ajax/', register_ajax, name='register_ajax'),
    path('login-ajax/', login_ajax, name='login_ajax'),
    path('logout-ajax/', logout_ajax, name='logout_ajax'),
]