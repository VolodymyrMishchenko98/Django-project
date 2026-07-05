from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('author/', views.author, name='author'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/add/', views.movie_add, name='movie_add'),
    path('movies/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('movies/edit/<int:pk>/', views.movie_edit, name='movie_edit'),
    path('movies/delete/<int:pk>/', views.movie_delete, name='movie_delete'),
    path('movies/<int:movie_pk>/comment/<int:comment_pk>/delete/', views.delete_comment, name='delete_comment'),
    path('movies/top/', views.movies_top, name='movies_top'),
]
