# МініБлог — Django проєкт (Лаби 2-8)

## КРОК 1: Початкове налаштування (PyCharm Terminal)

```bash
# Встановити залежності
pip install django pillow

# Створити superuser (адміна)
python manage.py createsuperuser

# Застосувати міграції
python manage.py makemigrations
python manage.py migrate

# Запустити сервер
python manage.py runserver
```

## КРОК 2: Наповнення через адмінку (Лаба 4)

1. Відкрити http://127.0.0.1:8000/admin/
2. Увійти як superuser
3. Додати 2-3 **Категорії** (поля: name, slug — заповнюється автоматично)
4. Додати 3-5 **Постів** (вибрати автора, категорію, вказати текст, можна додати фото)
5. Переглянути сайт: http://127.0.0.1:8000/

## КРОК 3: Git коміти по лабах

```bash
git init
git add .
git commit -m "Лаба 2: Створення Django проєкту miniblog"

# Підключити GitHub репозиторій (замінити YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/miniblog.git
git branch -M main
git push -u origin main
```

### Коміти по лабах (робити після кожної):
```bash
# Лаба 3
git add . && git commit -m "Лаба 3: Аплікація blog, шаблони, навігація"

# Лаба 4
git add . && git commit -m "Лаба 4: Моделі Category, Post, Comment, Rating, Newsletter. Адмін-панель"

# Лаба 5
git add . && git commit -m "Лаба 5: Хедер, футер, меню категорій, CSS, base.html"

# Лаба 6
git add . && git commit -m "Лаба 6: Сторінка категорії та посту з фотографіями"

# Лаба 7
git add . && git commit -m "Лаба 7: Коментарі, оцінки постів, форма розсилки"

# Лаба 8
git add . && git commit -m "Лаба 8: Реєстрація, вхід, вихід, профіль, зміна пароля через email"

git push
```

## Структура проєкту

```
miniblog/
├── manage.py
├── requirements.txt
├── db.sqlite3              ← створюється після migrate
├── media/                  ← фото постів
├── miniblog/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── blog/
    ├── models.py           ← Category, Post, Comment, Rating, Newsletter
    ├── views.py            ← всі в'юшки
    ├── urls.py             ← всі маршрути
    ├── forms.py            ← всі форми
    ├── admin.py            ← адмін-панель
    ├── static/blog/css/
    │   └── style.css       ← весь CSS тут (не в HTML!)
    └── templates/blog/
        ├── base.html       ← базовий шаблон (DRY)
        ├── home.html
        ├── about.html
        ├── contacts.html
        ├── category_detail.html
        ├── post_detail.html
        └── auth/
            ├── login.html
            ├── register.html
            ├── profile.html
            ├── change_password.html
            ├── password_reset_request.html
            └── password_reset_confirm.html
```

## Функціонал по лабах

| Лаба | Що реалізовано |
|------|----------------|
| 2    | Django проєкт, git init, перший пуш |
| 3    | Аплікація blog, 3 сторінки з навігацією, render + context |
| 4    | 5 моделей з зв'язками, адмін-панель з назвою/датами |
| 5    | Header з меню категорій, footer, CSS в окремому файлі, base.html |
| 6    | Сторінка категорії (тільки її пости), сторінка посту з фото |
| 7    | Коментарі (кошик аналог), розсилка (email форма), оцінки з середнім балом |
| 8    | Реєстрація, вхід, вихід, профіль, зміна пароля, відновлення через email-код |

## Важливі URL-и

| URL | Сторінка |
|-----|----------|
| / | Головна |
| /about/ | Про нас |
| /contacts/ | Контакти |
| /category/<slug>/ | Категорія |
| /post/<slug>/ | Пост |
| /login/ | Вхід |
| /register/ | Реєстрація |
| /logout/ | Вихід |
| /profile/ | Особистий кабінет |
| /change-password/ | Зміна пароля |
| /password-reset/ | Відновлення пароля |
| /admin/ | Адмін-панель |
