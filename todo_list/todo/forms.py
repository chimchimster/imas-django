from django import forms


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput())
    email = forms.CharField(label='Электронная почта', widget=forms.EmailInput())
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput())


class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput())
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())


class AddActionForm(forms.Form):
    title = forms.CharField(label='Заголовок', widget=forms.TextInput())
    content = forms.CharField(label='Контент', widget=forms.Textarea(attrs={'rows': 10, 'cols': 50}))