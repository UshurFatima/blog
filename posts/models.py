from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    is_active = models.BooleanField(default=True)
    view_count = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
