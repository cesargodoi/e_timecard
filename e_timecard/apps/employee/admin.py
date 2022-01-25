from django.contrib import admin, messages
from django.utils.translation import ngettext

from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    # actions
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            ngettext(
                "%d employee was successfully marked as 'inactive'.",
                "%d employees were successfully marked as 'inactives'.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            ngettext(
                "%d employee was successfully marked as 'active'.",
                "%d employees were successfully marked as 'actives'.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    make_inactive.short_description = "Mark selected employees as 'inactive'."
    make_active.short_description = "Mark selected employees as 'active'."

    actions = [make_inactive, make_active]

    # filters and others
    list_filter = ["employee_class"]
    search_fields = ["name", "company__corp_name", "company__name"]
    list_display = ["name", "reg", "employee_class", "is_active", "company"]

    readonly_fields = ("created_on", "modified_on", "made_by")
    fieldsets = [
        (
            None,
            {"fields": ["company", "reg"]},
        ),
        (
            "Personal Informations",
            {"fields": ["name", "id_card", "birth"]},
        ),
        (
            "Employee Informations",
            {"fields": ["employee_class", "observations"]},
        ),
        (
            "Auth Informations",
            {"fields": ["is_active", "created_on", "modified_on", "made_by"]},
        ),
    ]

    def save_model(self, request, obj, form, change):
        obj.made_by = request.user
        super().save_model(request, obj, form, change)
