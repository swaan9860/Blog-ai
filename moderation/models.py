# moderation/models.py
from django.db import models
from blog.models import Post
from django.contrib.auth import get_user_model

User = get_user_model()

class FlaggedContent(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='flags')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255)  # e.g., "Toxic content"
    score = models.FloatField()  # Confidence score from AI model
    flagged_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)  # Admin approval status

    def __str__(self):
        return f"Flag: {self.post.title} - {self.reason} ({self.score})"