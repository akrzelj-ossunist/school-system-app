from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    ROLES = (('prof', 'profesor'), ('stu', 'student'))
    STATUS = (('none', 'None'), ('izv', 'izvanredni student'), ('red', 'redovni student'))
    role = models.CharField(max_length=50, choices=ROLES)
    status = models.CharField(max_length=50, choices=STATUS)

class Subject(models.Model):
    IZBORNI = (('da', 'da'), ('ne', 'ne'))
    ime = models.CharField(max_length=50)
    kod = models.CharField(max_length=50)
    program = models.CharField(max_length=50)
    bodovi = models.IntegerField()
    sem_redovni = models.IntegerField()
    sem_izvanredni = models.IntegerField()
    izborni = models.CharField(max_length=50, choices=IZBORNI)
    nositelj = models.ForeignKey(User, limit_choices_to={'role': 'prof'}, on_delete=models.CASCADE, null=True)

class Upisi(models.Model):
    STATUS_UPISA = (('upisan', 'Upisan'), ('polozen', 'Polozen'), ('izgubio', 'Izgubio potpis'))
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    predmet = models.ForeignKey(Subject, on_delete=models.CASCADE)
    status_upisa = models.CharField(max_length=50, choices=STATUS_UPISA)