from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    birth_date = models.DateField()
    phone = models.CharField(max_length=20)

class Request(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Идёт обучение'),
        ('completed', 'Обучение завершено'),
    ]
    
    PAYMENT_CHOICES = [
        ('cash', 'Наличными'),
        ('transfer', 'Перевод по номеру'),
    ]
    
    TRANSPORT_CHOICES = [
        ('bus', 'Автобус'),
        ('electric_bus', 'Электробус'),
        ('tram', 'Трамвай'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transport_type = models.CharField(max_length=20, choices=TRANSPORT_CHOICES)
    start_date = models.DateField()
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_transport_type_display()}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request = models.OneToOneField(Request, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Отзыв от {self.user.username}"