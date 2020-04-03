from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q
from .models import Post, Author, PostView, AnonymousView
from .forms import CommentForm, PostForm, RegisterUser, ContactForm
from marketing.models import SignUp
from django.contrib import messages


def register_view(request):
  if request.user.is_authenticated:
    return redirect("/")
  else:
    next = request.GET.get('next')
    form = RegisterUser(request.POST or None)
    if form.is_valid():
      form.save()
      if next:
        return redirect(next)
      return redirect('account_login')
    
    context = {
      'form': form
    }
    return render(request, 'register.html', context)


def get_author(user):
  qs = Author.objects.filter(user=user)
  if qs.exists():
    return qs[0]
  return None


def get_category_count():
  queryset = Post.objects.values('categories__title').annotate(Count('categories__title'))
  return queryset


def index(request):
  featured = Post.objects.filter(featured=True)
  latest = Post.objects.order_by('-timestamp')[0:3]

  if request.method == 'POST':
    email = request.POST['email']
    new_email = SignUp()
    new_email.email = email
    new_email.save()
     
  context = {
    'object_list': featured,
    'latest': latest
  }
  return render(request, 'index.html', context)


def blog(request):
  category_count = get_category_count()
  most_recent = Post.objects.order_by('-timestamp')[:3]
  post_list = Post.objects.all().order_by('id')
  paginator = Paginator(post_list, 4)
  page_request_var = 'page'
  page = request.GET.get(page_request_var)

  try:
    paginated_queryset = paginator.page(page)
  except PageNotAnInteger:
    paginated_queryset = paginator.page(1)
  except EmptyPage:
    paginated_queryset = paginator.page(paginator.num_pages)

  context = {
    'queryset': paginated_queryset,
    'page_request_var': page_request_var,
    'most_recent': most_recent,
    'category_count': category_count
  }
  return render(request, 'blog.html', context)


def post(request, pk):
  category_count = get_category_count()
  most_recent = Post.objects.order_by('-timestamp')[:3]
  post = get_object_or_404(Post, pk=pk)

  if request.user.is_authenticated:
    PostView.objects.get_or_create(user=request.user, post=post)
  else:
    AnonymousView.objects.get_or_create(post=post)

  form = CommentForm(request.POST or None)
  if request.method == 'POST':
    form.instance.user = request.user
    form.instance.post = post
    form.save()
    return redirect('posts:post-detail', pk=pk)

  context = {
    'form': form,
    'post': post,
    'most_recent': most_recent,
    'category_count': category_count
  }
  return render(request, 'post.html', context)


def search(request):
  queryset = Post.objects.all()
  query = request.GET.get('q')

  if query:
    queryset = queryset.filter(
      Q(title__icontains = query) |
      Q(overview__icontains = query)
    ).distinct()
  
  context = {
    'queryset': queryset
  }
  return render(request, 'search-result.html', context)


def post_create(request):
  form = PostForm(request.POST or None, request.FILES or None)
  author = get_author(request.user)
  if request.method == 'POST':
    if form.is_valid():
      form.instance.author = author
      form.save()
      return redirect('posts:post-detail', pk=form.instance.pk)
  context = {
    'form': form,
    'title': 'Create'
  }
  return render(request, 'post-create.html', context)


def post_update(request, pk):
  post = get_object_or_404(Post,pk=pk)
  form = PostForm(request.POST or None, request.FILES or None, instance=post)
  author = get_author(request.user)
  if request.method == 'POST':
    if form.is_valid():
      form.instance.author = author
      form.save()
      return redirect('posts:post-detail', pk=form.instance.pk)
  context = {
    'form': form,
    'title': 'Update'
  }
  return render(request, 'post-create.html', context)


def post_delete(request, pk):
  post = get_object_or_404(Post, pk=pk)
  post.delete()
  return redirect('posts:blog')

def contact(request):
  form = ContactForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      form.save()
      form = ContactForm()
      messages.success(request, 'Your message has been sent')
    else:
      messages.warning(request, 'Please correct the errors below')

  context = {
    'form': form
  }
  return render(request, 'contact.html', context)