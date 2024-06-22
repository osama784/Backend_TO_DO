from django.db import models
from django.conf import settings


class Category(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name


class Task(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    body = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.SET_NULL, blank=True, null=True)
    is_done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created']