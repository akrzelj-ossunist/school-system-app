from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from .forms import CreateUser, CreateSubject, EditUser
from .models import Subject, User

@login_required
def home(request):
    return render(request, "./home.html", {'username':request.user})

def register(request):
    if request.method == 'GET':
        if request.user.is_superuser:
            userForm = CreateUser()
            return render(request, 'register.html', {'form': userForm})
        else:
            return redirect("/")
    if request.method == 'POST' and request.user.is_superuser:
        print("entered register post")
        userForm = CreateUser(request.POST)
        if userForm.is_valid():
            userForm.save()
            return redirect("/")
        else:
            return render(request, 'register.html', {'form': userForm})
    else:
        return HttpResponseNotAllowed('Unable to register')
    
def add_subject(request):
    if request.method == "GET":
        if request.user.is_superuser:
            subjectForm = CreateSubject()
            return render(request, "./addsubject.html", {'form': subjectForm})
        else:
            return redirect("/")
    if request.method == "POST" and request.user.is_superuser:
        subjectForm = CreateSubject(request.POST)
        if subjectForm.is_valid():
            subjectForm.save()
            return redirect("/")
        else:
            return render(request, "./addsubject.html", {'form': subjectForm})
    else:
        return HttpResponseNotAllowed('Unable to register')
    
def subject_list(request):
    if request.user.is_superuser:
        subjects = Subject.objects.all()
        return render(request, './subjectlist.html', {'subjects': subjects})
    
def edit_subject(request, id):
    subject = Subject.objects.get(pk=id)
    if request.method == 'GET' and request.user.is_superuser:
        editForm = CreateSubject(instance=subject)
        return render(request, 'editSubject.html', {'form': editForm})
    if request.method == 'POST' and request.user.is_superuser:
        editForm = CreateSubject(request.POST, instance=subject)
        if editForm.is_valid():
            editForm.save()
        return redirect('/subjects')
    
def user_list(request, role):
    if request.user.is_superuser:
        users = User.objects.all().filter(role=role)
        return render(request, './userlist.html', {'users': users})
    
def edit_user(request, id):
    user = User.objects.get(pk=id)
    if request.method == 'GET' and request.user.is_superuser:
        editForm = EditUser(instance=user)
        return render(request, 'edituser.html', {'form': editForm})
    if request.method == 'POST' and request.user.is_superuser:
        editForm = EditUser(request.POST, instance=user)
        if editForm.is_valid():
            editForm.save()
    return redirect('/user_list/stu') if user.role == 'stu' else redirect('/user_list/prof')