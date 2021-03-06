# Generated by Django 3.2.11 on 2022-01-25 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='country',
            field=models.CharField(choices=[('BR', 'Brazil'), ('US', 'United States')], default='BR', max_length=2),
        ),
        migrations.AlterField(
            model_name='company',
            name='eni',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='company',
            name='phone_1',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='company',
            name='phone_2',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='company',
            name='state',
            field=models.CharField(blank=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='company',
            name='zip_code',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
