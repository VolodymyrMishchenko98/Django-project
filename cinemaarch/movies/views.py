from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Movie
from .forms import MovieForm, CommentForm


def home(request):
    """Головна сторінка сайту"""
    top_movies = Movie.objects.all().order_by('-rating', '-year')[:4]
    return render(request, 'home.html', {'top_movies': top_movies})


def author(request):
    """Сторінка про автора"""
    return render(request, 'author.html')


def movie_list(request):
    """Сторінка зі списком фільмів з фільтрацією, пошуком та сортуванням"""
    movies = Movie.objects.all().distinct()
    genres = Movie.objects.values_list('genre', flat=True).distinct()
    search_query = request.GET.get('search', '').strip()
    genre_filter = request.GET.get('genre', '').strip()
    sort_option = request.GET.get('sort', '').strip()
    
    # Пошук за назвою (case-insensitive, partial match)
    if search_query:
        movies = movies.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
    
    # Фільтр за жанром
    if genre_filter:
        movies = movies.filter(genre=genre_filter)
    
    # Сортування
    if sort_option == 'year_asc':
        movies = movies.order_by('year')
    elif sort_option == 'year_desc':
        movies = movies.order_by('-year')
    
    context = {
        'movies': movies,
        'genres': sorted(genres),
        'search_query': search_query,
        'genre_filter': genre_filter,
        'sort_option': sort_option,
        'total_found': movies.count(),
    }
    return render(request, 'movies.html', context)


def movie_detail(request, pk):
    """Детальна інформація про фільм"""
    movie = get_object_or_404(Movie, pk=pk)
    # Збільшити лічильник переглядів
    if request.method == 'GET': # Increment views only on GET requests
        movie.increment_views()

    comments = movie.comments.all() # Получаем все комментарии к фильму

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.movie = movie
            new_comment.save()
            messages.success(request, 'Ваш коментар успішно додано!')
            return redirect('movie_detail', pk=movie.pk)
    else:
        comment_form = CommentForm()
    return render(request, 'movie_detail.html', {'movie': movie, 'comments': comments, 'comment_form': comment_form})


def movie_add(request):
    """Додавання нового фільму"""
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Фільм успішно додано!')
            return redirect('movie_list')
    else:
        form = MovieForm()
    return render(request, 'movie_form.html', {'form': form, 'title': 'Додати фільм'})


def movie_edit(request, pk):
    """Редагування фільму"""
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            messages.success(request, 'Фільм успішно оновлено!')
            return redirect('movie_list')
    else:
        form = MovieForm(instance=movie)
    return render(request, 'movie_form.html', {'form': form, 'title': 'Редагувати фільм'})


def movie_delete(request, pk):
    """Видалення фільму"""
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        movie.delete()
        messages.success(request, 'Фільм успішно видалено!')
        return redirect('movie_list')
    return render(request, 'movie_confirm_delete.html', {'movie': movie})

def movies_top(request):
    """Топ фільмів"""
    movies = Movie.objects.all().order_by('-rating', '-year')[:10]
    return render(request, 'movies_top.html', {'movies': movies})