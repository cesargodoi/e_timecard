# Generated by Django 3.2.11 on 2022-01-25 07:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0002_auto_20220125_0432'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('reg', models.CharField(blank=True, max_length=15, null=True)),
                ('name', models.CharField(max_length=100)),
                ('name_sa', models.CharField(editable=False, max_length=100)),
                ('id_card', models.CharField(blank=True, max_length=30, verbose_name='id card')),
                ('birth', models.DateField(blank=True, null=True)),
                ('employee_class', models.CharField(choices=[('SEN', 'Senior'), ('TRN', 'Trainee'), ('FRE', 'Freelancer'), ('VOL', 'Volunteer')], default='SEN', max_length=3)),
                ('observations', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='company.company')),
                ('made_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='made_by_employee', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'employee',
                'verbose_name_plural': 'employees',
            },
        ),
    ]
