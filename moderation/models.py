# moderation/models.py

from django.db import models
from blog.models import Post
from django.contrib.auth import get_user_model

User = get_user_model()

class FlaggedContent(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='flags')
    reason = models.CharField(max_length=255)
    score = models.FloatField()
    flagged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-flagged_at']  # ← Fixed: use flagged_at, not created_at
        verbose_name = "Flagged Content"
        verbose_name_plural = "Flagged Contents"

    def __str__(self):
        return f"Flag on {self.post.title}: {self.reason} ({self.score})"