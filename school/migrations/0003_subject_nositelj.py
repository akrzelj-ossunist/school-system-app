# Generated by Django 4.2.2 on 2023-06-24 13:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_subject_upisi'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='nositelj',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
