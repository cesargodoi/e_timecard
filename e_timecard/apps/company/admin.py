from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_filter = ["country", "state", "city"]
    search_fields = ["corp_name", "name", "eni"]
    list_display = [
        "corp_name",
        "name",
        "phone_1",
        "phone_2",
        "email",
    ]
    readonly_fields = ("created_on", "modified_on", "made_by")
    fieldsets = [
        (
            None,
            {"fields": ["corp_name", "name", "eni"]},
        ),
        (
            "Contact Informations",
            {"fields": ["phone_1", "phone_2", "email"]},
        ),
        (
            "Address Informations",
            {
                "fields": [
                    "address",
                    "number",
                    "complement",
                    "district",
                    "city",
                    "state",
                    "country",
                    "zip_code",
                ]
            },
        ),
        (
            "Other Informations",
            {"fields": ["observations"]},
        ),
        (
            "Auth Informations",
            {"fields": ["is_active", "created_on", "modified_on", "made_by"]},
        ),
    ]

    def save_model(self, request, obj, form, change):
        obj.made_by = request.user
        super().save_model(request, obj, form, change)
