from django.contrib import admin
from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'director', 'year', 'genre', 'rating_display', 'watched_display', 'views', 'created_at')
    list_filter = ('year', 'genre', 'rating', 'watched', 'created_at')
    search_fields = ('title', 'director', 'description', 'genre')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'views')
    
    fieldsets = (
        ('Основна інформація', {
            'fields': ('title', 'director', 'description', 'genre', 'year', 'poster')
        }),
        ('Оцінка та Статус', {
            'fields': ('rating', 'watched', 'views')
        }),
        ('Мета-інформація', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def rating_display(self, obj):
        if obj.rating:
            stars = '⭐' * obj.rating
            return f"{stars} ({obj.rating}/10)"
        return "-"
    rating_display.short_description = 'Рейтинг'
    
    def watched_display(self, obj):
        if obj.watched:
            return '✓ Переглянуто'
        return '✕ Не переглянуто'
    watched_display.short_description = 'Статус'