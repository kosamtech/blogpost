from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from tinymce import HTMLField

User = get_user_model()

class Author(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  profile_pic = models.ImageField()

  def __str__(self):
    return self.user.username


class Category(models.Model):
  title = models.CharField(max_length=20)

  def __str__(self):
    return self.title


class PostView(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  post = models.ForeignKey('Post', on_delete=models.CASCADE)

  def __str__(self):
    return self.user.username


class AnonymousView(models.Model):
  post = models.ForeignKey('Post', on_delete=models.CASCADE)

  def __str__(self):
    return self.post.title


class Comment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  timestamp = models.DateTimeField(auto_now_add=True)
  post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
  content = models.TextField()
  
  def __str__(self):
    return self.user.username


class Post(models.Model):
  title = models.CharField(max_length=200)
  overview = models.TextField()
  author = models.ForeignKey(Author, on_delete=models.CASCADE)
  thumbnail = models.ImageField()
  categories = models.ManyToManyField(Category)
  previous_post = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='previous', null=True, blank=True)
  next_post = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='next', null=True, blank=True)
  content = HTMLField()
  timestamp = models.DateTimeField(auto_now_add=True)
  featured = models.BooleanField(default=True) 

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('posts:post-detail', kwargs={'pk': self.pk})

  def get_post_update(self):
    return reverse('posts:post-update', kwargs={'pk': self.pk})

  def get_post_delete(self):
    return reverse('posts:post-delete', kwargs={'pk': self.pk})

  @property
  def get_comments(self):
    return self.comments.all().order_by('-timestamp')

  @property
  def view_count(self):
    return PostView.objects.filter(post=self).count()

  @property
  def anonymous_view(self):
    return AnonymousView.objects.filter(post=self).count()

  @property
  def comment_count(self):
    return Comment.objects.filter(post=self).count()


class Contact(models.Model):
  username = models.CharField(max_length=100)
  email = models.EmailField()
  message = models.TextField()

  def __str__(self):
    return self.username