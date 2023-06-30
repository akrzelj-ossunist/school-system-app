from django.forms import ModelForm, forms
from .models import User, Subject
from django.contrib.auth.forms import UserCreationForm

class CreateUser(UserCreationForm):
  class Meta:
    model = User
    fields = ["username", "email", "password1", "password2", "role", "status"]

class CreateSubject(ModelForm):
  class Meta:
    model = Subject
    fields = ["ime", "kod", "program", "bodovi", "sem_redovni", "sem_izvanredni", "izborni"]

class EditUser(ModelForm):
  class Meta:
    model = User
    fields = ['username', 'email', 'role', 'status']

class TeacherForm(ModelForm):
  class Meta:
    model = Subject
    fields = ["nositelj"]