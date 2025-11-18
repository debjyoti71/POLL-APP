from django.db import models
import uuid
from django.utils.text import slugify

class Poll(models.Model):
    question = models.CharField(max_length=255)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    slug = models.SlugField(unique=True, blank=True)
    private_code = models.UUIDField(default=uuid.uuid4, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.question)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.question


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.text} ({self.votes} votes)"
