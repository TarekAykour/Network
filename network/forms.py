from .models import Post
from django.forms import ModelForm
from django import forms

class Create_post(ModelForm):
   class Meta:    
        model = Post
        fields = ['message']