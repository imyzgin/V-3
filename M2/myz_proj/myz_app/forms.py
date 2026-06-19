from django import forms
from django.forms import Textarea
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from datetime import date
import re

class RegisterForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=150)
    full_name = forms.CharField(label='ФИО', max_length=200)
    birth_date = forms.DateField(label='Дата рождения', widget=forms.DateInput(attrs={'type': 'date'}))
    phone = forms.CharField(label='Контактный телефон', max_length=20)
    email = forms.EmailField(label='E-mail')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)
    
    def clean_username(self):
        username = self.cleaned_data['username']
        
        if not re.match(r'^[a-zA-Z0-9]+$', username):
            raise ValidationError('Логин должен содержать только латинские буквы и цифры')
        
        if len(username) < 6:
            raise ValidationError('Логин должен быть не менее 6 символов')
        
        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким логином уже существует')
        
        return username
    
    def clean_password1(self):
        password = self.cleaned_data['password1']
        
        if len(password) < 8:
            raise ValidationError('Пароль должен быть не менее 8 символов')
        
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError('Пароли не совпадают')

class RequestForm(forms.Form):
    transport_type = forms.ChoiceField(label='Вид транспорта', choices=[
        ('bus', 'Автобус'),
        ('electric_bus', 'Электробус'),
        ('tram', 'Трамвай'),
    ])
    start_date = forms.DateField(label='Дата начала обучения', widget=forms.DateInput(attrs={'type': 'date'}))
    payment_method = forms.ChoiceField(label='Способ оплаты', choices=[
        ('cash', 'Наличными'),
        ('transfer', 'Перевод по номеру'),
    ])
    
    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        today = date.today()
        
        if start_date < today:
            raise ValidationError('Дата начала не может быть раньше сегодняшнего дня')
        
        return start_date

class ReviewForm(forms.Form):
    rating = forms.ChoiceField(label='Оценка', choices=[
        (1, '1 - Ужасно'),
        (2, '2 - Плохо'),
        (3, '3 - Нормально'),
        (4, '4 - Хорошо'),
        (5, '5 - Отлично'),
    ])
    text = forms.CharField(label='Отзыв', max_length=500, widget=Textarea)