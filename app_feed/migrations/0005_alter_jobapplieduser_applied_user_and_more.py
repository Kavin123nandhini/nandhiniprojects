# Generated by Django 4.1.3 on 2023-09-04 17:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_restapi', '0002_userregistration_about_company'),
        ('app_feed', '0004_alter_joblisting_posted_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplieduser',
            name='applied_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applied_user', to='app_restapi.userregistration'),
        ),
        migrations.AlterField(
            model_name='joblisting',
            name='posted_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='joblisting', to='app_restapi.userregistration'),
        ),
    ]
