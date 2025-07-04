from django import forms
from .models import Post, User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['postContent', ]
        widgets = {
            'postContent': forms.Textarea(attrs={
                'rows': 3,
                'autofocus': True,
                'class': 'w-full px-3 py-2 border border-gray-700 rounded bg-gray-900 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-800 transition resize-none',
                'placeholder': 'What\'s on your mind?'
            })
        }
        labels = {
            'postContent': 'New Post'
        }


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'block w-full px-3 py-2 border border-gray-700 bg-gray-900 text-gray-100 rounded-t-md focus:outline-none focus:ring-2 focus:ring-blue-700 focus:border-blue-700 transition',
        'placeholder': 'Password'
    }))
    confirmation = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'block w-full px-3 py-2 border border-gray-700 bg-gray-900 text-gray-100 rounded-b-md focus:outline-none focus:ring-2 focus:ring-blue-700 focus:border-blue-700 transition',
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'profile_picture']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-700 bg-gray-900 text-gray-100 rounded-t-md focus:outline-none focus:ring-2 focus:ring-blue-700 focus:border-blue-700 transition',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-700 bg-gray-900 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-700 focus:border-blue-700 transition',
                'placeholder': 'Email'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-700 bg-gray-900 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-700 focus:border-blue-700 transition resize-none',
                'placeholder': 'Bio (optional)',
                'rows': 2
            }),
            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'file:mr-4 file:rounded-full file:border-0 file:bg-blue-50 file:px-4 file:py-2 file:text-sm file:font-semibold file:text-blue-700 hover:file:bg-blue-100 dark:file:bg-blue-600 dark:file:text-blue-100 dark:hover:file:bg-blue-500'
            }),
        }