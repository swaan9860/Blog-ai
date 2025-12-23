# blog/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse
from taggit.managers import TaggableManager  # Make sure django-taggit is installed and in INSTALLED_APPS

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    content = models.TextField()
    picture = models.ImageField(upload_to="post_pictures/", blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Useful for tracking edits
    tags = TaggableManager(blank=True)  # For tag-based filtering and recommendations
    is_published = models.BooleanField(default=True)  # For moderation: False if flagged/toxic

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['slug']),
            models.Index(fields=['is_published']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            self.slug = base_slug
            counter = 1
            while Post.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)


class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="preference")
    preferred_tags = TaggableManager(blank=True)

    class Meta:
        verbose_name = "User Preference"
        verbose_name_plural = "User Preferences"

    def __str__(self):
        return f"{self.user.username}'s preferences"


class PostInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='postinteraction')
    viewed = models.BooleanField(default=False)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")
        ordering = ['-viewed_at']
        indexes = [
            models.Index(fields=['user', 'viewed']),
            models.Index(fields=['post']),
        ]

    def __str__(self):
        return f"{self.user.username} viewed {self.post.title}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)  # Optional: let users add a bio
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return None  # Or return a default avatar URL
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"