from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Post
import requests

# Create your views here.
def index(request):
  # return HttpResponse('route works correctly')
  post = Post.objects.all()[:10]

  print(post)

  context = {
    'title': 'Lastest Post',
    'posts': post
  }

  return render(request, 'posts/index.html', context)


def details(request, id):
  try:
    post = Post.objects.get(id = id)
  except:
    raise Http404

  context = {
    'post' : post 
  }

  return render(request, 'posts/details.html', context)

def courses(request):
  r = requests.get('http://kiu.counties-hub.com/api/courses')
  print(r.content)
  context = {
    'courses': r.content
  }
  return render(request, 'posts/courses.html', context)