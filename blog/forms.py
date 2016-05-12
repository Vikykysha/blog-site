from django import forms
from .models import Post, Comment, Tag
from django.contrib.auth.models import User
from blog.models import UserProfile, Category
from django.contrib.auth.models import User

class PostForm(forms.Form):

   
    title = forms.CharField(label="Title of the post",max_length=100)
    text= forms.CharField(label="Text of your post",widget=forms.Textarea)
    category = forms.ModelChoiceField(label="Select category",queryset=Category.objects.all(),required=False)
    tags = forms.CharField(label="Select or add your tag",widget=forms.TextInput(attrs={'id':'myinput'}),required=False)
    
    
      
   
  

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ( 'text',)
         
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    def clean_email(self):
            email = self.cleaned_data["email"]
      
            user = User.objects.filter(email=email)
            if user.exists():             
               raise forms.ValidationError("This email address already exists. Did you forget your password?")
            else:
          
               return email
            return email
        

  
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'hobby')
         


