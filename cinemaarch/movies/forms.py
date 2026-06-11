from django import forms
from .models import Movie, Comment


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'director', 'description', 'genre', 'year', 'poster', 'rating', 'watched']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введіть назву фільму'
            }),
            'director': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введіть ім’я режисера'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введіть опис фільму',
                'rows': 4
            }),
            'genre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введіть жанр'
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1888,
                'max': 2100,
                'placeholder': 'Введіть рік випуску'
            }),
            'poster': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,
                'placeholder': 'Оцінка від 1 до 10'
            }),
            'watched': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            }),
        }
        labels = {
            'title': 'Назва фільму',
            'director': 'Режисер',
            'description': 'Опис',
            'genre': 'Жанр',
            'year': 'Рік випуску',
            'poster': 'Постер',
            'rating': 'Рейтинг (1-10)',
            'watched': 'Я переглянув(ла) цей фільм',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']
        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше ім’я'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Напишіть коментар...', 'rows': 4}),
        }
        labels = {
            'author': 'Ваше ім’я',
            'text': 'Коментар',
        }