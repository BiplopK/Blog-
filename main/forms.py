from django import forms 
from django.contrib import messages
from .models import *
from django_ckeditor_5.widgets import CKEditor5Widget

class BlogPostForm(forms.ModelForm):

    class Meta:
        model = BlogPost
        fields = ['blog_title','category','content']
        widgets = {
            'blog_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'category': forms.Select(attrs={'class': 'form-control', 'placeholder':'Choose Category'}),
            'content': CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="extends"
              ),
        }





class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields=['content']
        widget={
            'content': forms.Textarea(attrs={'rows':3, 'placeholder':"Add a comments...."})
        }
    
class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['profile_pics']
        widgets = {
            'profile_pics': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

class UpdateuserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
    