# posts/urls.py
from django.urls import path
from . import views

# Эта строчка обязательна.
# Без неё namespace работать не будет:
app_name = 'posts'


urlpatterns = [
    path('', views.index, name='index'),
    path('group/<slug:slug>/', views.group_posts, name='group_list')
]
