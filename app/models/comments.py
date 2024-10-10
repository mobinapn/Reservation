from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Comment(models.Model):
    event = models.ForeignKey('Event', related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Comment by {self.user} on {self.event}"

    def is_reply(self):
        return self.parent is not None
