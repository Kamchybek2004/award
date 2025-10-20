from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth import login
from django.db.models import Q
from .forms import EmployerSearchForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import UserRegisterForm, EmployerForm, AwardForm
from .models import Employer, Award, STATE_AWARDS, HONORARY_TITLES


def register(request):
    """Регистрация пользователя + создание Employer"""
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # создаём пустой профиль Employer
            Employer.objects.create(user=user)
            login(request, user)  # сразу авторизуем
            messages.success(request, "Регистрация успешна! Заполните профиль сотрудника.")
            return redirect("employer:dashboard")
    else:
        form = UserRegisterForm()
    return render(request, "employer/register.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = 'employer/login.html'


@login_required
def dashboard(request):
    """Личный кабинет сотрудника"""
    employer, created = Employer.objects.get_or_create(user=request.user)
    return render(request, "employer/dashboard.html", {"employer": employer})


@login_required
def edit_profile(request):
    """Редактирование профиля сотрудника"""
    employer, created = Employer.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = EmployerForm(request.POST, instance=employer)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлён.")
            return redirect("employer:dashboard")
    else:
        form = EmployerForm(instance=employer)
    return render(request, "employer/edit_profile.html", {"form": form})


class EmployerDetailView(DetailView):
    model = Employer
    template_name = "employer/employer_detail.html"
    context_object_name = "employer"


# ================= Награды ================= #

@login_required
def add_award(request):
    """Добавление награды сотрудником"""
    employer, created = Employer.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = AwardForm(request.POST)
        if form.is_valid():
            award = form.save(commit=False)
            award.employer = employer
            award.save()
            messages.success(request, "Награда добавлена!")
            return redirect("employer:dashboard")
    else:
        form = AwardForm()
    return render(request, "employer/award_form.html", {"form": form, "title": "Добавить награду"})


@login_required
def edit_award(request, pk):
    """Редактирование своей награды"""
    employer, created = Employer.objects.get_or_create(user=request.user)
    award = get_object_or_404(Award, pk=pk, employer=employer)
    if request.method == "POST":
        form = AwardForm(request.POST, instance=award)
        if form.is_valid():
            form.save()
            messages.success(request, "Награда обновлена!")
            return redirect("employer:dashboard")
    else:
        form = AwardForm(instance=award)
    return render(request, "employer/award_form.html", {"form": form, "title": "Редактировать награду"})


@login_required
def delete_award(request, pk):
    """Удаление награды"""
    employer, created = Employer.objects.get_or_create(user=request.user)
    award = get_object_or_404(Award, pk=pk, employer=employer)
    if request.method == "POST":
        award.delete()
        messages.success(request, "Награда удалена.")
        return redirect("employer:dashboard")
    return render(request, "employer/confirm_delete.html", {"award": award})


# ================= Публичная часть ================= #

def employer_list(request):
    """Список всех сотрудников с наградами (публичная страница)"""
    employers = Employer.objects.prefetch_related("awards").all()

    # Исключаем "пустых" сотрудников (у кого все поля None или пустые)
    employers = employers.exclude(
        (Q(last_name__isnull=True) | Q(last_name="")) &
        (Q(first_name__isnull=True) | Q(first_name="")) &
        (Q(middle_name__isnull=True) | Q(middle_name="")) &
        (Q(birth_date__isnull=True)) &
        (Q(position__isnull=True) | Q(position="")) &
        (Q(department__isnull=True) | Q(department="")) &
        (Q(faculty__isnull=True) | Q(faculty="")) &
        (Q(hire_date__isnull=True))
    )

    faculty = request.GET.get("faculty")    
    hire_date = request.GET.get("hire_date")
    department = request.GET.get("department")
    award_filter = request.GET.get("award")  

    if faculty:
        employers = employers.filter(faculty=faculty)
    
    if hire_date:
        employers = employers.filter(hire_date__year=hire_date)
    
    if department:
        employers = employers.filter(department=department)

    
      # --- Фильтрация по наградам ---
    if award_filter == "state":
        employers = employers.filter(awards__type="state")
    elif award_filter == "department":
        employers = employers.filter(awards__type="department")

    employers = employers.distinct()
    faculty_codes = Employer.objects.values_list("faculty", flat=True).distinct()

    faculty_choices = dict(Employer._meta.get_field("faculty").choices)
    faculties = [(code, faculty_choices.get(code, code)) for code in faculty_codes if code]

    departments = Employer.objects.values_list("department", flat=True).distinct()
    years_qs = Employer.objects.dates("hire_date", "year", order="DESC")
    years = [y.year for y in years_qs]

    return render(request, "employer/employer_list.html", {
        "employers": employers,
        "faculties": faculties,
        "departments": departments,
        "years": years,
        })


def employer_search(request):
    raw_query = request.GET.get('query', '').strip()
    query = raw_query.lower()
    results = []

    if query:
        for emp in Employer.objects.all():
            # формируем строку с ФИО и должностью
            searchable = " ".join(filter(None, [
                emp.first_name,
                emp.last_name,
                emp.middle_name,
                emp.position
            ])).lower()

            if all(word in searchable for word in query.split()):
                results.append(emp)

    context = {
        'results': results,
        'query': raw_query,
    }
    return render(request, 'employer/employer_search.html', context)
