# CineVault

Персональний архів фільмів на Django з реєстрацією, коментарями та підтримкою деплою на Render.

## Стек

- Python / Django
- SQLite — локально
- PostgreSQL — на Render
- Django Templates + статика CSS
- Render для деплою

## Локальний запуск

```powershell
cd C:\Users\user\OneDrive\Desktop\Django-project-main\cinemaarch

python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Відкрити: `http://127.0.0.1:8000`

## Функціонал

- Каталог фільмів з пошуком, фільтрами та сортуванням
- Додавання / редагування / видалення фільмів — тільки для авторизованих
- Реєстрація та вхід:
  - `/accounts/register/`
  - `/accounts/login/`
  - `/accounts/logout/`
  - `/login/`, `/register/`, `/logout/`
- Коментарі до фільмів:
  - додавати можуть лише авторизовані
  - видаляти — лише автор коментаря
- Профіль користувача: `/profile/` або `/profile/<username>/`

## Деплой на Render

### Підготовка

- `build.sh` — в корені проєкту
- `requirements.txt` — залежності
- `render.yaml` — конфіг для Render

### Кроки

1. Підготувати проєкт і завантажити на GitHub
2. Створити PostgreSQL на Render
3. Створити Web Service:
   - Build Command: `./build.sh`
   - Start Command: `gunicorn cinemaarch.cinemaarch.wsgi:application`
   - Instance Type: Free
4. Додати змінні середовища:
   - `PYTHON_VERSION` = `3.11.9`
   - `SECRET_KEY` = довгий випадковий рядок
   - `DATABASE_URL` = з бази даних Render → Connect → Internal Database URL
5. Після деплою створити суперюзера через Render Shell:

```powershell
python manage.py createsuperuser
```

## Примітки

- Локально використовується SQLite
- На Render — PostgreSQL через `dj_database_url`
- `STATIC_ROOT` = `staticfiles/`
- Медіа — `media/`
