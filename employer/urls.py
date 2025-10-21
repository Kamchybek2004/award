# employer/urls.py
from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth import views as auth_views  # <-- добавь это
from . import views
from .views import EmployerDetailView

app_name = "employer"

urlpatterns = [
    # Аутентификация
    path("register/", views.register, name="register"),
    path("login/", LoginView.as_view(template_name="employer/login.html"), name="login"),
     path('logout/', auth_views.LogoutView.as_view(next_page='employer:login'), name='logout'),

    # Личный кабинет
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),

    # Награды
    path("award/add/", views.add_award, name="add_award"),
    path("award/<int:pk>/edit/", views.edit_award, name="edit_award"),
    path("award/<int:pk>/delete/", views.delete_award, name="delete_award"),

    # Публичная часть
    path("", views.employer_list, name="employer_list"),

    # Поиск 
    path('search/', views.employer_search, name='employer_search'),
    path("employer/<int:pk>/", EmployerDetailView.as_view(), name="employer_detail"),
    path("search-award/", views.award_search_view, name="award_search"),
]
