# Generated by Django 4.0.5 on 2023-06-27 17:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_subject_nositelj'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='nositelj',
            field=models.ForeignKey(limit_choices_to={'role': 'prof'}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
