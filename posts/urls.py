from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
  path('', views.index, name='index'),
  path('blog/', views.blog, name='blog'),
  path('post/<str:pk>/', views.post, name='post-detail'),
  path('post/create', views.post_create, name='post-create'),
  path('post/<str:pk>/update', views.post_update, name='post-update'),
  path('post/<str:pk>/delete', views.post_delete, name='post-delete'),
  path('search/', views.search, name='search'),
]