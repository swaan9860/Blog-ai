# blog/forms.py

from django import forms
from .models import Post, UserPreference, UserProfile, Comment
from taggit.forms import TagWidget
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'picture', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a catchy title...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Write your post content here...'
            }),
            'picture': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'tags': TagWidget(attrs={
                'class': 'form-control',
                'placeholder': 'Add tags (e.g. travel, tech, food)'
            }),
        }
        labels = {
            'title': 'Title',
            'content': 'Content',
            'picture': 'Featured Image (optional)',
            'tags': 'Tags',
        }


class CommentForm(forms.ModelForm):
    """
    Now a ModelForm so it has .save() method.
    Used for both new comments and replies.
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment...',
                'required': 'required'
            }),
        }
        labels = {
            'content': '',
        }


class UserPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserPreference
        fields = ['preferred_tags']
        widgets = {
            'preferred_tags': TagWidget(attrs={
                'class': 'form-control',
                'placeholder': 'Add tags you like (e.g. technology, health, food)'
            }),
        }
        labels = {
            'preferred_tags': 'Preferred Tags',
        }


class AvatarUploadForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']
        widgets = {
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'avatar': 'Choose Avatar',
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'username': 'Username',
            'email': 'Email Address',
        }