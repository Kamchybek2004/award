# employer/admin.py
from django.contrib import admin
from .models import Employer, Award

@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "position", "faculty")
    search_fields = ("last_name", "first_name", "middle_name", "position", "faculty")
    list_filter = ("faculty", "department")


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ("__str__", "employer", "type", "award_date", "issued_by")
    list_filter = ("type", "award_date")
    search_fields = ("title", "issued_by", "document_number")
    autocomplete_fields = ("employer",)
