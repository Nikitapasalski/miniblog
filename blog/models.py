from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    """Категорія постів"""
    name = models.CharField(max_length=100, verbose_name='Назва категорії')
    slug = models.SlugField(unique=True, verbose_name='URL')
    description = models.TextField(blank=True, verbose_name='Опис')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Створено о')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Оновлено о')

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        ordering = ['name']

    def __str__(self):
        return self.name


class Post(models.Model):
    """Пост блогу"""
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, verbose_name='URL')
    content = models.TextField(verbose_name='Зміст')
    image = models.ImageField(upload_to='posts/', blank=True, null=True, verbose_name='Зображення')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='posts', verbose_name='Категорія')
    is_published = models.BooleanField(default=True, verbose_name='Опублікований')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Створено о')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Оновлено о')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Пости'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(r.score for r in ratings) / ratings.count(), 1)
        return None

    def rating_count(self):
        return self.ratings.count()


class Comment(models.Model):
    """Коментар до посту"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                              related_name='comments', verbose_name='Пост')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    content = models.TextField(verbose_name='Текст коментаря')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Створено о')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Оновлено о')

    class Meta:
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'
        ordering = ['-created_at']

    def __str__(self):
        return f'Коментар від {self.author.username} до "{self.post.title}"'


class Rating(models.Model):
    """Оцінка посту"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                              related_name='ratings', verbose_name='Пост')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Користувач')
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Оцінка (1-5)'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Створено о')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Оновлено о')

    class Meta:
        verbose_name = 'Оцінка'
        verbose_name_plural = 'Оцінки'
        unique_together = ('post', 'user')  # один юзер — одна оцінка на пост

    def __str__(self):
        return f'{self.user.username} → {self.post.title}: {self.score}/5'


class Newsletter(models.Model):
    """Підписка на розсилку"""
    email = models.EmailField(unique=True, verbose_name='Email')
    name = models.CharField(max_length=100, blank=True, verbose_name='Ім\'я')
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name='Створено о')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Оновлено о')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        verbose_name = 'Підписник'
        verbose_name_plural = 'Підписники'
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email
