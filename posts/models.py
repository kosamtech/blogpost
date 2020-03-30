from django.db import models
import datetime

# Create your models here.
class Post(models.Model):
  title = models.CharField(max_length=200)
  body = models.TextField()
  created_at = models.DateTimeField(datetime.datetime.now(), blank=True)

  def __str__(self):
    return self.title

  class Meta:
    verbose_name_plural = "Post"
