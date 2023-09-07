# Generated by Django 4.1.3 on 2023-09-04 06:21

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRegistration',
            fields=[
                ('user_reg_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('emirates_id', models.CharField(max_length=200, unique=True)),
                ('user_role', models.CharField(max_length=30, null=True)),
                ('emirates_office', models.CharField(max_length=30, null=True)),
                ('phonenumber', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator('^[0-9+]', 'Only digit characters.')])),
                ('qualification', models.CharField(blank=True, max_length=30, null=True)),
                ('university', models.CharField(blank=True, max_length=30, null=True)),
                ('year_passed_out', models.CharField(blank=True, max_length=30, null=True)),
                ('skills', models.CharField(blank=True, max_length=500, null=True)),
                ('exp_years', models.CharField(blank=True, max_length=30, null=True)),
                ('designation', models.CharField(blank=True, max_length=30, null=True)),
                ('work_company', models.CharField(blank=True, max_length=30, null=True)),
                ('total_employees', models.CharField(blank=True, max_length=30, null=True)),
                ('auth_name', models.CharField(blank=True, max_length=30, null=True)),
                ('date_of_registration', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]