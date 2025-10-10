import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Employer, Award


class UserRegisterForm(UserCreationForm):
    """Форма регистрации пользователя + базовые поля профиля"""
    email = forms.EmailField(
        label="Электронная почта",
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'})
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        # Проверка на кириллицу
        if re.search(r'[а-яА-ЯёЁ]', password):
            raise forms.ValidationError("Пароль не должен содержать кириллицу. Используйте только латиницу, цифры и спецсимволы.")
        return password


class EmployerForm(forms.ModelForm):
    """Редактирование профиля сотрудника"""
    class Meta:
        model = Employer
        fields = [
            'last_name', 'first_name', 'middle_name',
            'birth_date', 'position', 'department',
            'faculty', 'hire_date'
        ]
        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'faculty': forms.TextInput(attrs={'class': 'form-control'}),
            'hire_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class AwardForm(forms.ModelForm):
    """Добавление/редактирование награды"""
    class Meta:
        model = Award
        fields = [
            'type', 'state_award', 'honorary_title',
            'title', 'award_date', 'issued_by',
            'document_number', 'description'
        ]
        widgets = {
            'type': forms.Select(attrs={'class': 'form-select', 'id': 'id_type'}),
            'state_award': forms.Select(attrs={'class': 'form-select', 'id': 'id_state_award'}),
            'honorary_title': forms.Select(attrs={'class': 'form-select', 'id': 'id_honorary_title'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_title'}),
            'award_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'issued_by': forms.TextInput(attrs={'class': 'form-control'}),
            'document_number': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        """Валидация: правильное заполнение награды"""
        cleaned_data = super().clean()
        type = cleaned_data.get("type")

        if type == 'state' and not cleaned_data.get("state_award"):
            self.add_error("state_award", "Укажите государственную награду.")   
        if type == 'honorary' and not cleaned_data.get("honorary_title"):
            self.add_error("honorary_title", "Укажите почётное звание.")
        if type == 'department' and not cleaned_data.get("title"):
            self.add_error("title", "Укажите название ведомственной награды.")

        return cleaned_data



class EmployerSearchForm(forms.Form):
    query = forms.CharField(label='Поиск', max_length=100, required=False)