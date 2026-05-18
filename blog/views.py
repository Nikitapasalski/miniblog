from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random
import string

from .models import Category, Post, Comment, Rating, Newsletter
from .forms import (
    CommentForm, RatingForm, NewsletterForm,
    RegisterForm, LoginForm, CustomPasswordChangeForm,
    PasswordResetRequestForm, PasswordResetConfirmForm
)


# ─── ЛАБА 3/5: Головна та загальні сторінки ──────────────────────────────────

def home(request):
    """Головна сторінка"""
    categories = Category.objects.all()
    posts = Post.objects.filter(is_published=True).select_related('author', 'category')

    selected_category = request.GET.get('category')
    if selected_category:
        posts = posts.filter(category__slug=selected_category)

    newsletter_form = NewsletterForm()

    context = {
        'title': 'МініБлог — Головна',
        'posts': posts,
        'categories': categories,
        'selected_category': selected_category,
        'newsletter_form': newsletter_form,
    }
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html', {
        'title': 'Про нас',
        'categories': Category.objects.all(),
    })


def contacts(request):
    return render(request, 'blog/contacts.html', {
        'title': 'Контакти',
        'categories': Category.objects.all(),
    })


# ─── ЛАБА 6: Сторінка категорії та посту ─────────────────────────────────────

def category_detail(request, slug):
    """Сторінка категорії з постами"""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, is_published=True).select_related('author')
    context = {
        'title': f'Категорія: {category.name}',
        'category': category,
        'posts': posts,
        'categories': Category.objects.all(),
    }
    return render(request, 'blog/category_detail.html', context)


def post_detail(request, slug):
    """Сторінка окремого посту"""
    post = get_object_or_404(Post, slug=slug, is_published=True)
    comments = post.comments.select_related('author').order_by('-created_at')
    avg_rating = post.average_rating()
    rating_count = post.rating_count()

    # Перевіряємо чи поточний юзер вже оцінював
    user_rating = None
    if request.user.is_authenticated:
        try:
            user_rating = Rating.objects.get(post=post, user=request.user)
        except Rating.DoesNotExist:
            pass

    comment_form = CommentForm()
    rating_form = RatingForm()
    newsletter_form = NewsletterForm()

    context = {
        'title': post.title,
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'rating_form': rating_form,
        'newsletter_form': newsletter_form,
        'avg_rating': avg_rating,
        'rating_count': rating_count,
        'user_rating': user_rating,
        'categories': Category.objects.all(),
    }
    return render(request, 'blog/post_detail.html', context)


# ─── ЛАБА 7: Коментарі, оцінки, розсилка ─────────────────────────────────────

@login_required
def add_comment(request, slug):
    """Додати коментар"""
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Коментар додано!')
    return redirect('post_detail', slug=slug)


@login_required
def rate_post(request, slug):
    """Оцінити пост"""
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            score = int(form.cleaned_data['score'])
            rating, created = Rating.objects.update_or_create(
                post=post, user=request.user,
                defaults={'score': score}
            )
            if created:
                messages.success(request, f'Ви оцінили пост на {score}/5!')
            else:
                messages.success(request, f'Вашу оцінку оновлено: {score}/5!')
    return redirect('post_detail', slug=slug)


def subscribe_newsletter(request):
    """Підписка на розсилку"""
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if Newsletter.objects.filter(email=email).exists():
                messages.info(request, 'Ви вже підписані на розсилку!')
            else:
                form.save()
                messages.success(request, 'Дякуємо! Ви успішно підписалися на розсилку.')
        else:
            messages.error(request, 'Невірний email.')
    return redirect(request.META.get('HTTP_REFERER', '/'))


# ─── ЛАБА 8: Аутентифікація ───────────────────────────────────────────────────

def register_view(request):
    """Реєстрація"""
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Вітаємо, {user.username}! Реєстрація успішна.')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'blog/auth/register.html', {
        'title': 'Реєстрація',
        'form': form,
        'categories': Category.objects.all(),
    })


def login_view(request):
    """Вхід"""
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Ласкаво просимо, {user.username}!')
            return redirect(request.GET.get('next', 'home'))
    else:
        form = LoginForm()
    return render(request, 'blog/auth/login.html', {
        'title': 'Вхід',
        'form': form,
        'categories': Category.objects.all(),
    })


@login_required
def logout_view(request):
    """Вихід"""
    logout(request)
    messages.info(request, 'Ви вийшли з акаунту.')
    return redirect('home')


@login_required
def profile_view(request):
    """Особистий кабінет"""
    user = request.user
    if user.is_staff:
        # Адмін бачить всі коментарі
        comments = Comment.objects.select_related('post', 'author').order_by('-created_at')
        title = 'Адмін-панель: всі коментарі'
    else:
        # Звичайний юзер бачить свої коментарі
        comments = Comment.objects.filter(author=user).select_related('post').order_by('-created_at')
        title = 'Мій кабінет'

    user_ratings = Rating.objects.filter(user=user).select_related('post')

    context = {
        'title': title,
        'comments': comments,
        'user_ratings': user_ratings,
        'categories': Category.objects.all(),
    }
    return render(request, 'blog/auth/profile.html', context)


@login_required
def change_password_view(request):
    """Зміна пароля (авторизований юзер)"""
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль успішно змінено!')
            return redirect('profile')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'blog/auth/change_password.html', {
        'title': 'Зміна пароля',
        'form': form,
        'categories': Category.objects.all(),
    })


def password_reset_request(request):
    """Крок 1: Запит скидання пароля — надсилаємо код на email"""
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                # Генеруємо 6-значний код
                code = ''.join(random.choices(string.digits, k=6))
                # Зберігаємо в сесії
                request.session['reset_code'] = code
                request.session['reset_user_id'] = user.id
                # Надсилаємо email (в консоль при DEBUG)
                send_mail(
                    subject='МініБлог — Код відновлення пароля',
                    message=f'Ваш код для відновлення пароля: {code}\n\nКод дійсний 10 хвилин.',
                    from_email='noreply@miniblog.com',
                    recipient_list=[email],
                )
                messages.success(request, f'Код надіслано на {email}. Перевірте пошту (або консоль PyCharm).')
                return redirect('password_reset_confirm')
            except User.DoesNotExist:
                messages.error(request, 'Користувача з таким email не знайдено.')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'blog/auth/password_reset_request.html', {
        'title': 'Відновлення пароля',
        'form': form,
        'categories': Category.objects.all(),
    })


def password_reset_confirm(request):
    """Крок 2: Підтвердження коду та встановлення нового пароля"""
    if request.method == 'POST':
        form = PasswordResetConfirmForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            new_password = form.cleaned_data['new_password']
            session_code = request.session.get('reset_code')
            user_id = request.session.get('reset_user_id')

            if code == session_code and user_id:
                try:
                    user = User.objects.get(id=user_id)
                    user.set_password(new_password)
                    user.save()
                    # Видаляємо код з сесії
                    del request.session['reset_code']
                    del request.session['reset_user_id']
                    messages.success(request, 'Пароль успішно змінено! Увійдіть з новим паролем.')
                    return redirect('login')
                except User.DoesNotExist:
                    messages.error(request, 'Помилка. Спробуйте знову.')
            else:
                messages.error(request, 'Невірний код! Спробуйте знову.')
    else:
        form = PasswordResetConfirmForm()
    return render(request, 'blog/auth/password_reset_confirm.html', {
        'title': 'Введіть код',
        'form': form,
        'categories': Category.objects.all(),
    })
