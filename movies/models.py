from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, max_length=500)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    avatar_color = models.CharField(max_length=7, default='#2b5ce6')

    def __str__(self):
        return f'Профіль {self.user.username}'

    def get_initials(self):
        fn = self.user.first_name
        ln = self.user.last_name
        if fn and ln:
            return f'{fn[0]}{ln[0]}'.upper()
        return self.user.username[:2].upper()


class Movie(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва фільму")
    director = models.CharField(max_length=100, verbose_name="Режисер")
    description = models.TextField(verbose_name="Опис")
    genre = models.CharField(max_length=100, verbose_name="Жанр")
    year = models.IntegerField(verbose_name="Рік випуску")
    poster = models.ImageField(upload_to='posters/', verbose_name="Постер")
    rating = models.PositiveSmallIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Рейтинг"
    )
    watched = models.BooleanField(default=False, verbose_name="Переглянуто")
    views = models.PositiveIntegerField(default=0, verbose_name="Кількість переглядів")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата додавання")

    class Meta:
        verbose_name = "Фільм"
        verbose_name_plural = "Фільми"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def increment_views(self):
        self.views = models.F('views') + 1
        self.save(update_fields=['views'])
        self.refresh_from_db()


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Коментар від {self.author.username} до {self.movie.title}'


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='watchlist_entries')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')
        ordering = ['-added_at']

    def __str__(self):
        return f'{self.user.username} — {self.movie.title}'
