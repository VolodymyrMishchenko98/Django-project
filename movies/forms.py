from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Movie, Comment


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    first_name = forms.CharField(
        required=False,
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ім\'я'})
    )
    last_name = forms.CharField(
        required=False,
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Прізвище'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логін'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Пароль'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Підтвердження пароля'})


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логін або email', 'autofocus': True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'director', 'description', 'genre', 'year', 'poster', 'rating', 'watched']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть назву фільму'}),
            'director': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть ім\'я режисера'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введіть опис фільму', 'rows': 4}),
            'genre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть жанр'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'min': 1888, 'max': 2100, 'placeholder': 'Введіть рік випуску'}),
            'poster': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10, 'placeholder': 'Оцінка від 1 до 10'}),
            'watched': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
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
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Напишіть коментар...', 'rows': 4}),
        }
        labels = {
            'text': 'Коментар',
        }
