# BlogAI/blog/admin.py
from django.contrib import admin
from .models import Post, UserPreference, PostInteraction, Profile

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'is_published']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'content']
    list_per_page = 25

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_preferred_tags']
    search_fields = ['user__username']

    def get_preferred_tags(self, obj):
        return ", ".join(obj.preferred_tags.names()) or "None"
    get_preferred_tags.short_description = 'Preferred Tags'

@admin.register(PostInteraction)
class PostInteractionAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'viewed']
    list_filter = ['viewed']
    search_fields = ['user__username', 'post__title']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'avatar']
    search_fields = ['user__username']