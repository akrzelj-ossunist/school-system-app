from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from .forms import CreateUser, CreateSubject, EditUser, TeacherForm
from .models import Subject, User, Upisi

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
    if request.user.is_superuser or request.user.role == 'stu':
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

def assign_teacher(request, id):
    subject = Subject.objects.get(pk=id)
    if request.method == 'GET' and request.user.is_superuser:
        form = TeacherForm(instance=subject)
        return render(request, './assignTeacher.html', {'form': form})
    if request.method == "POST" and request.user.is_superuser:
        form = TeacherForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect("/subjects")
        else:
            return render(request, "./assignTeacher.html", {'form': form})
    else:
        return HttpResponseNotAllowed('Unable to register')

def enrollment_form(request, id):
  if request.user.is_superuser or request.user.id == id:
    user = User.objects.get(pk=id)
    upisi = Upisi.objects.filter(student=user)
    subjects = Subject.objects.all()
    non_enrolled = []
    enrolled = []
    is_erolled = False
    year_one_ects=0
    year_two_ects=0
    for subject in subjects:
        for upis in upisi:
            if upis.predmet_id == subject.id:
                is_erolled = True
        if is_erolled:
            is_erolled = False
        else:
            non_enrolled.append(subject)
    for upis in upisi:
        subject_name = Subject.objects.get(id=upis.predmet_id)
        if subject_name.sem_redovni == 1 or subject_name.sem_redovni == 2:
            if upis.status_upisa == 'polozen':
                year_one_ects+=subject_name.bodovi
        if subject_name.sem_redovni == 3 or subject_name.sem_redovni == 4:
            if upis.status_upisa == 'polozen':
                year_one_ects+=subject_name.bodovi
        enrolled.append({'id': upis.id,'status_upisa': upis.status_upisa, 'predmet': subject_name.ime})
    # check if all 1st year subjects are passed
    subjects = Subject.objects.filter(sem_redovni__lt=3)
    allow_enroll=True
    for subject in subjects:
        upis = Upisi.objects.filter(student_id=id, predmet_id=subject.id)
        if len(upis) == 0:
            allow_enroll=False
            break
        if upis[0].status_upisa != 'polozen':
            allow_enroll=False
            break
    print(allow_enroll)
    return render(request, 'enrollment.html', {'enrolled': enrolled, 'subjects': non_enrolled, 'uid': id, 'year_one': year_one_ects, 'year_two': year_two_ects, 'allow_enroll': allow_enroll})
  
def enroll(request, uid, sid):
  if request.user.is_superuser or request.user.id == uid:
    predmet = Subject.objects.get(pk=sid)
    korisnik = User.objects.get(pk=uid)
    Upisi.objects.create(student=korisnik, predmet=predmet, status_upisa='upisan')
  if request.user.role == 'stu':
    return redirect('/')  
  else:
    return redirect('/user_list/stu')

def disenroll(request, upisni_id, user_id):
    if request.user.is_superuser or request.user.id == user_id:
        predmet = Upisi.objects.get(pk=upisni_id)
        predmet.delete()
    if request.user.role == 'stu':
        return redirect('/')  
    else:
        return redirect('/user_list/stu')

def students_on_subject(request, id):
    if request.user.is_superuser or request.user.role == 'prof':
        subject = Subject.objects.get(pk=id)
        students_id = Upisi.objects.filter(predmet_id=subject.id)
        users = User.objects.all()
        students=[]
        status=False
        for user in users:
            for stu in students_id:
                if stu.student_id == user.id:
                    status=True
            if status:
                status = Upisi.objects.get(predmet_id=id, student_id=user.id)
                new_user = {
                    'pred_status': status.status_upisa,
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                    'status': user.status,
                }
                students.append(new_user)
                status=False
        return render(request, './userlist.html', {'users': students, 'sid': id})
    
def my_subjects(request, id):
    if request.user.role == 'prof':
        subjects = Subject.objects.filter(nositelj_id=id)
        return render(request, './subjectlist.html', {'subjects': subjects})
    
def edit_status(request, uid, sid, status):
    predmet = Subject.objects.get(pk=sid)
    korisnik = User.objects.get(pk=uid)
    if request.user.role == 'prof':
        upis = Upisi.objects.get(predmet=predmet, student=korisnik)
        upis.status_upisa = status
        upis.save()
    return redirect('students_on_subject', id=sid)

def filter_by_status(request, sid, status):
    if request.user.role == 'prof':
        predmet = Subject.objects.get(pk=sid)
        users = User.objects.all()
        upisi = Upisi.objects.filter(predmet=predmet, status_upisa=status)
        val=False
        students=[]
        for user in users:
            for upis in upisi:
                if upis.student_id == user.id:
                    val = True
            if val:
                new_user = {
                    'pred_status': status,
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                    'status': user.status,
                }
                students.append(new_user)
                val=False
        return render(request, './userlist.html', {'users': students, 'sid': sid})
            
def delete_subject(request, sid):
    if request.user.is_superuser:
        predmet = Subject.objects.get(pk=sid)
        predmet.delete()
    return redirect('/')

def delete_user(request, uid):
    if request.user.is_superuser:
        user = User.objects.get(pk=uid)
        user.delete()
    return redirect('/')

def last_year_students(request):
    if request.user.is_superuser:
        students = User.objects.filter(role='stu')
        val=False
        users=[]
        for student in students:
            upisani_predmeti = Upisi.objects.filter(student_id=student.id)
            for predmet in upisani_predmeti:
                p = Subject.objects.get(id=predmet.predmet_id)
                if p.sem_redovni == 5 or p.sem_redovni == 6:
                    val=True
            if val:
                val=False
                users.append(student)
        return render(request, './userlist.html', {'users': users})


def predmeti_po_statusu(request, uid, status, izborni):
    if request.user.id == uid:
        upisi = Upisi.objects.filter(student_id=uid, status_upisa=status)
        subjects = Subject.objects.filter(izborni=izborni)
        val=False
        subjects_list=[]
        for subject in subjects:
            for upis in upisi:
                if subject.id == upis.predmet_id:
                    val=True
            if val:
                subjects_list.append(subject)
                val=False
        return render(request, './subjectlist.html', {'subjects': subjects_list })

def filter_subjects(request):
    if request.user.role == 'stu':
        if request.method == 'POST':
            if request.POST['ects']:
                ects = request.POST['ects']
            else:
                ects = 1
            if request.POST['semestar']:
                subjects = Subject.objects.filter(bodovi__gt=ects, sem_redovni=request.POST['semestar'])
            else:
                subjects = Subject.objects.filter(bodovi__gt=ects)
            return render(request, './subjectlist.html', {'subjects': subjects })
        return render(request, "./filtersubjects.html")
        
    
def upisani_nepolozeni(request, uid):
    if request.user.role == 'stu':
        upisi = Upisi.objects.filter(student_id=uid, status_upisa='upisan')
        subjects = Subject.objects.filter(bodovi__gt=6)
        val=False
        subjects_list=[]
        for subject in subjects:
            for upis in upisi:
                if subject.id == upis.predmet_id:
                    val=True
            if val:
                subjects_list.append(subject)
                val=False
        return render(request, './subjectlist.html', {'subjects': subjects_list })


        
