from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from tinymce import TinyMCE 
from .models import Post, Comment, Contact


User = get_user_model()


class RegisterUser(UserCreationForm):
  username = forms.CharField(widget=forms.TextInput(attrs={
    'class': 'form-control',
    'placeholder': 'Username'
  }))
  email = forms.CharField(widget=forms.EmailInput(attrs={
    'class': 'form-control',
    'placeholder': 'someone@gmail.com'
  }))
  password1 = forms.CharField(widget=forms.PasswordInput(attrs={
    'class': 'form-control',
    'placeholder': 'Password'
  }))
  password2 = forms.CharField(widget=forms.PasswordInput(attrs={
    'class': 'form-control',
    'placeholder': 'Confirm Password'
  }))

  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']



class TinyMCEWidget(TinyMCE):
  def use_required_attribute(self, *args):
    return False


class PostForm(forms.ModelForm):
  content = forms.CharField(widget=TinyMCEWidget(attrs={
    'required': False,
    'cols': 30,
    'rows': 10
  }))

  class Meta:
    model = Post
    fields = ['title', 'overview', 'thumbnail', 'categories', 'previous_post', 'next_post', 'content', 'featured']


class CommentForm(forms.ModelForm):
  content = forms.CharField(widget=forms.Textarea(attrs={
    'class': 'form-control',
    'placeholder': 'Type your comment here',
    'id': 'usercomment',
    'rows': 4
  }))

  class Meta:
    model = Comment
    fields = ['content']

class ContactForm(forms.ModelForm):
  class Meta:
    model = Contact
    fields = '__all__'