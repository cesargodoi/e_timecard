import uuid

from django.conf import settings
from django.db import models
from e_timecard.apps.core.utils import COUNTRIES, phone_format

# Company
class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    eni = models.CharField(max_length=20, blank=True)  # cnpj
    corp_name = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=50, blank=True)
    number = models.CharField(max_length=10, blank=True)
    complement = models.CharField(max_length=50, blank=True)
    district = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=2, blank=True)
    country = models.CharField(max_length=2, choices=COUNTRIES, default="BR")
    zip_code = models.CharField(max_length=15, blank=True)
    phone_1 = models.CharField(max_length=20, blank=True)
    phone_2 = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=60, blank=True)
    observations = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    made_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="made_by_center",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        self.state = str(self.state).upper()
        self.phone_1 = phone_format(self.phone_1)
        self.phone_2 = phone_format(self.phone_2)
        super(Company, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.corp_name} ({self.name} - {self.country})"

    class Meta:
        verbose_name = "company"
        verbose_name_plural = "companies"
        ordering = ["name"]
