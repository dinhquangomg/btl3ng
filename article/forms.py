from django import forms
from .models import Post

class PostCreateForm(forms.ModelForm):
    tag = forms.CharField()
    class Meta:
        model = Post
        fields = ['title', 'content', 'thumbnail']

