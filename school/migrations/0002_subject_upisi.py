# Generated by Django 4.0.5 on 2023-06-23 17:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ime', models.CharField(max_length=50)),
                ('kod', models.CharField(max_length=50)),
                ('program', models.CharField(max_length=50)),
                ('bodovi', models.IntegerField()),
                ('sem_redovni', models.IntegerField()),
                ('sem_izvanredni', models.IntegerField()),
                ('izborni', models.CharField(choices=[('da', 'da'), ('ne', 'ne')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Upisi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_upisa', models.CharField(choices=[('upisan', 'Upisan'), ('polozen', 'Polozen'), ('izgubio', 'Izgubio potpis')], max_length=50)),
                ('predmet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.subject')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]