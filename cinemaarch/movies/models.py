from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


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
        """Increment the view counter by 1"""
        self.views = models.F('views') + 1
        self.save(update_fields=['views'])
        self.refresh_from_db()


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=50)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
