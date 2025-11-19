from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    super_user = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split('@')[0]
        super().save(*args, **kwargs)
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)



class Poll(models.Model):
    question = models.CharField(max_length=255)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='polls', null=True, blank=True)

    slug = models.SlugField(unique=True, blank=True)
    private_code = models.UUIDField(default=uuid.uuid4, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.question)
            slug = base_slug
            counter = 1
            while Poll.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.question



class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.text} ({self.votes} votes)"


class VoteRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'poll')   # user can vote only once

