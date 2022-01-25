import uuid

from django.conf import settings
from django.db import models
from e_timecard.apps.core.utils import EMPLOYEE_CLASS, us_inter_char

# from user.models import User


# Employee
class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(
        "company.Company",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    reg = models.CharField(max_length=15, null=True, blank=True)
    name = models.CharField(max_length=100)
    name_sa = models.CharField(max_length=100, editable=False)
    id_card = models.CharField("id card", max_length=30, blank=True)
    birth = models.DateField(null=True, blank=True)
    employee_class = models.CharField(
        max_length=3, choices=EMPLOYEE_CLASS, default="SEN"
    )
    observations = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    made_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="made_by_employee",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def clean(self, *args, **kwargs):
        super(Employee, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f"<<{self.user.email.split('@')[0]}>>"
        self.name_sa = us_inter_char(self.name)
        super(Employee, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - ({self.company})"

    class Meta:
        verbose_name = "employee"
        verbose_name_plural = "employees"
