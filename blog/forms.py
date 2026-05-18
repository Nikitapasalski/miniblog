from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Comment, Rating, Newsletter


class CommentForm(forms.ModelForm):
    """Форма коментаря"""
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Напишіть свій коментар...',
                'class': 'form-control'
            })
        }
        labels = {'content': 'Коментар'}


class RatingForm(forms.ModelForm):
    """Форма оцінки посту"""
    SCORE_CHOICES = [(i, f'{i} ★') for i in range(1, 6)]
    score = forms.ChoiceField(
        choices=SCORE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'rating-radio'}),
        label='Ваша оцінка'
    )

    class Meta:
        model = Rating
        fields = ['score']


class NewsletterForm(forms.ModelForm):
    """Форма підписки на розсилку"""
    class Meta:
        model = Newsletter
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше ім\'я', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ваш email', 'class': 'form-control'}),
        }
        labels = {
            'name': 'Ім\'я',
            'email': 'Email',
        }


class RegisterForm(UserCreationForm):
    """Форма реєстрації"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=50, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Ім\'я', 'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Логін', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Пароль'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Повторіть пароль'})


class LoginForm(AuthenticationForm):
    """Форма входу"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Логін'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Пароль'})


class CustomPasswordChangeForm(PasswordChangeForm):
    """Форма зміни пароля"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class PasswordResetRequestForm(forms.Form):
    """Форма запиту скидання пароля"""
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ваш email'})
    )


class PasswordResetConfirmForm(forms.Form):
    """Форма підтвердження нового пароля через код"""
    code = forms.CharField(
        max_length=6,
        label='Код з email',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '6-значний код'})
    )
    new_password = forms.CharField(
        label='Новий пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Новий пароль'})
    )
    new_password2 = forms.CharField(
        label='Повторіть пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторіть пароль'})
    )

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('new_password')
        p2 = cleaned_data.get('new_password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Паролі не співпадають!')
        return cleaned_data
