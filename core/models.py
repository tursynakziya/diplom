from django.db import models
from django.contrib.auth.models import User


class ConvertedFile(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='files'
    )
    title = models.CharField(max_length=255)
    original_pdf = models.FileField(upload_to='uploads/')
    converted_audio = models.FileField(
        upload_to='audio/', blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"