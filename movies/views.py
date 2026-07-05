from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Profile, Movie, Comment
from .forms import MovieForm, CommentForm, RegisterForm, LoginForm


def get_or_create_profile(user):
    profile, _ = Profile.objects.get_or_create(user=user)
    return profile


def home(request):
    top_movies = Movie.objects.all().order_by('-rating', '-year')[:6]
    return render(request, 'home.html', {'top_movies': top_movies})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('movie_list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            get_or_create_profile(user)
            login(request, user)
            messages.success(request, f'Вітаємо, {user.username}! Реєстрація успішна.')
            return redirect('movie_list')
        messages.error(request, 'Будь ласка, виправте помилки у формі.')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('movie_list')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'З поверненням, {user.first_name or user.username}!')
            return redirect(request.GET.get('next', 'movie_list'))
        messages.error(request, 'Невірний логін або пароль.')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Ви успішно вийшли з системи.')
    return redirect('login')


def author(request):
    return render(request, 'author.html')


def movie_list(request):
    movies = Movie.objects.all().distinct()
    genres = Movie.objects.values_list('genre', flat=True).distinct()
    search_query = request.GET.get('search', '').strip()
    genre_filter = request.GET.get('genre', '').strip()
    sort_option = request.GET.get('sort', '').strip()

    if search_query:
        movies = movies.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

    if genre_filter:
        movies = movies.filter(genre=genre_filter)

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
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'GET':
        movie.increment_views()

    comments = movie.comments.all().select_related('author')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Для додавання коментаря потрібно увійти.')
            return redirect('login')
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.movie = movie
            new_comment.author = request.user
            new_comment.save()
            messages.success(request, 'Ваш коментар успішно додано!')
            return redirect('movie_detail', pk=movie.pk)
    else:
        comment_form = CommentForm()
    return render(request, 'movie_detail.html', {'movie': movie, 'comments': comments, 'comment_form': comment_form})


@login_required
def movie_add(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Фільм успішно додано!')
            return redirect('movie_list')
    else:
        form = MovieForm()
    return render(request, 'movie_form.html', {'form': form, 'title': 'Додати фільм'})


@login_required
def movie_edit(request, pk):
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


@login_required
def movie_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        movie.delete()
        messages.success(request, 'Фільм успішно видалено!')
        return redirect('movie_list')
    return render(request, 'movie_confirm_delete.html', {'movie': movie})


@login_required
def delete_comment(request, movie_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user != comment.author:
        messages.error(request, 'Ви не можете видалити чужий коментар.')
        return redirect('movie_detail', pk=movie_pk)
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Коментар видалено.')
    return redirect('movie_detail', pk=movie_pk)


def movies_top(request):
    movies = Movie.objects.all().order_by('-rating', '-year')[:10]
    return render(request, 'movies_top.html', {'movies': movies})
