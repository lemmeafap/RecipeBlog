from django import forms
from .models import Recipe, Comment
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'content',
            'photo',
            'is_published',
            'category',
            'time_to_cook'
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Название',
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Описание',
                'class': 'form-control'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'time_to_cook': forms.TextInput(attrs={
                'class': 'form-control'
            })
        }


class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=50, help_text='Максимум 50 символов',
                               label='Имя пользователя',
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'
                               }))

    password1 = forms.CharField(label='Новый пароль',
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Пароль'
                                }))

    password2 = forms.CharField(label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Подтвердите пароль'
                                }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите свою действительную почту'
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control'
                               }))

    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control'
                               }))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Оставить комментарий',
                'class': 'form-control'
            }),
        }
