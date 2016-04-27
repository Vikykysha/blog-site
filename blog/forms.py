from django import forms
from .models import Post, Comment
from django.contrib.auth.models import User
from blog.models import UserProfile

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'category','tags')

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ( 'text',)
         
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'hobby')
         


