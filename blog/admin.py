# blog/admin.py
from django.contrib import admin
from .models import Post, UserPreference, PostInteraction, UserProfile



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'is_published']
    search_fields = ['title', 'content']
    list_per_page = 25


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_preferred_tags']
    search_fields = ['user__username']

    def get_preferred_tags(self, obj):
        return ", ".join([t.name for t in obj.preferred_tags.all()]) or "None"
    get_preferred_tags.short_description = 'Preferred Tags'


@admin.register(PostInteraction)
class PostInteractionAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'viewed']
    list_filter = ['viewed']
    search_fields = ['user__username', 'post__title']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'avatar']
    search_fields = ['user__username']