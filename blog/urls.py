from django.urls import path
from . import views

urlpatterns = [
    # Лаба 3/5: Основні сторінки
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),

    # Лаба 6: Категорія та пост
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),

    # Лаба 7: Коментарі, оцінки, розсилка
    path('post/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('post/<slug:slug>/rate/', views.rate_post, name='rate_post'),
    path('newsletter/subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),

    # Лаба 8: Аутентифікація
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset/confirm/', views.password_reset_confirm, name='password_reset_confirm'),
]
