"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from school.views import home, upisani_nepolozeni, register, add_subject, subject_list, edit_subject, user_list, edit_user, assign_teacher, enrollment_form, enroll, disenroll, students_on_subject, my_subjects, edit_status, filter_by_status,delete_subject, delete_user, predmeti_po_statusu, last_year_students, filter_subjects
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('register/', register),
    path('add_subject/', add_subject),
    path('subjects/', subject_list),
    path('edit_subject/<int:id>', edit_subject, name='edit_subject'),
    path('delete_subject/<int:sid>', delete_subject, name='delete_subject'),
    path('user_list/<str:role>', user_list, name='user_list'),
    path('edit_user/<int:id>', edit_user, name='edit_user'),
    path('delete_user/<int:uid>', delete_user, name='delete_user'),
    path('assign_teacher/<int:id>', assign_teacher, name='assign_teacher'),
    path('enrollment_form/<int:id>', enrollment_form, name='enrollment_form'),
    path('enroll/<int:uid>/<int:sid>/', enroll, name='enroll'),
    path('disenroll/<int:upisni_id>/<int:user_id>/', disenroll, name='disenroll'),
    path('students_on_subject/<int:id>', students_on_subject, name='students_on_subject'),
    path('filter_by_status/<int:sid>/<str:status>', filter_by_status, name='filter_by_status'),
    path('my_subjects/<int:id>', my_subjects, name='my_subjects'),
    path('edit_status/<int:uid>/<int:sid>/<str:status>', edit_status, name='edit_status'),
    path('predmeti_po_statusu/<int:uid>/<str:status>/<str:izborni>', predmeti_po_statusu, name='predmeti_po_statusu'),
    path('last_year_students/', last_year_students, name='last_year_students'),
    path('filter_subjects', filter_subjects, name='filter_subjects'),
    path('upisani_nepolozeni/<int:uid>', upisani_nepolozeni, name='upisani_nepolozeni'),
]
