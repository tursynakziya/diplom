from django.db import models
from django.contrib.auth.models import User


class ConvertedFile(models.Model):
    CONVERSION_TYPES = [
        ('tts', 'Мәтін → Аудио'),
        ('subtitles', 'Видео → Субтитрлер'),
        ('ocr', 'Сурет → Мәтін'),
        ('large_text', 'Үлкен мәтін'),
        ('braille', 'Мәтін → Брайль'),
        ('audio_text', 'Аудио → Мәтін'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='files'
    )
    title = models.CharField(max_length=255)
    conversion_type = models.CharField(
        max_length=20, choices=CONVERSION_TYPES, default='tts'
    )

    # Кіріс файл
    original_file = models.FileField(
        upload_to='uploads/', blank=True, null=True
    )

    # Шығыс файлдар (конвертация түріне байланысты)
    converted_audio = models.FileField(
        upload_to='audio/', blank=True, null=True
    )
    converted_subtitle = models.FileField(
        upload_to='subtitles/', blank=True, null=True
    )
    converted_large_pdf = models.FileField(
        upload_to='large_text/', blank=True, null=True
    )
    converted_text = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_conversion_type_display()}) - {self.user.username}"

    class Meta:
        ordering = ['-created_at']

class Notification(models.Model):
    """Пайдаланушыларға жіберілген хабарламалар"""
    subject = models.CharField(max_length=255)
    message = models.TextField()
    recipient = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='notifications'
    )  # None болса — барлығына жіберілген
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['-created_at']


class UserMessage(models.Model):
    """Пайдаланушыдан админге жіберілген хабарламалар"""
    STATUS_CHOICES = [
        ('new', 'Жаңа'),
        ('read', 'Оқылған'),
        ('replied', 'Жауап берілген'),
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    subject = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    reply = models.TextField(blank=True, null=True)
    replied_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.subject}"

    class Meta:
        ordering = ['-created_at']


class UserProfile(models.Model):
    """Пайдаланушының мүмкіндіктері туралы профиль"""
    DISABILITY_CHOICES = [
        ('visual', 'Көру қабілеті шектеулі'),
        ('hearing', 'Есту қабілеті шектеулі'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    disability_type = models.CharField(
        max_length=10, choices=DISABILITY_CHOICES, default='visual'
    )

    def __str__(self):
        return f"{self.user.username} — {self.get_disability_type_display()}"

    @property
    def show_visual_tools(self):
        return self.disability_type == 'visual'

    @property
    def show_hearing_tools(self):
        return self.disability_type == 'hearing'


class SystemSettings(models.Model):
    """Жүйе параметрлері"""
    tts_voice = models.CharField(max_length=100, default='kk-KZ-AigulNeural')
    default_lang = models.CharField(max_length=10, default='kk')
    whisper_model = models.CharField(max_length=20, default='base')
    max_file_size = models.IntegerField(default=100)  # МБ

    class Meta:
        verbose_name = 'Жүйе параметрлері'

    def __str__(self):
        return 'Жүйе параметрлері'