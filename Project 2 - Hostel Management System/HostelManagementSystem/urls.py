"""HostelManagementSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from hostel.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('user_login',user_login, name='user_login'),
    path('user_home', user_home, name='user_home'),
    path('book_Hostel', book_Hostel, name='book_Hostel'),
    path('room_Details', room_Details, name='room_Details'),
    path('delete_RoomDtls/<int:pid>', delete_RoomDtls, name='delete_RoomDtls'),
    path('view_RoomDtls/<int:pid>', view_RoomDtls, name='view_RoomDtls'),
    path('my_Profile', my_Profile, name='my_Profile'),
    path('edit_profile', edit_profile, name='edit_profile'),
    path('change_UserPassword', change_UserPassword, name='change_UserPassword'),
    path('admin_home', admin_home, name='admin_home'),
    path('admin_login', admin_login, name='admin_login'),
    path('add_Room', add_Room, name='add_Room'),
    path('manage_Room', manage_Room, name='manage_Room'),
    path('edit_Room/<int:pid>', edit_Room, name='edit_Room'),
    path('delete_Room/<int:pid>', delete_Room, name='delete_Room'),
    path('student_Registration', student_Registration, name='student_Registration'),
    path('manage_student', manage_student, name='manage_student'),
    path('view_RegistrationDtls/<int:pid>', view_RegistrationDtls, name='view_RegistrationDtls'),
    path('changePassword', changePassword, name='changePassword'),
    path('logout',Logout,name='logout'),
    path('delete_StudentReg/<int:pid>', delete_StudentReg, name='delete_StudentReg'),
    path('search_students/', search_students, name='search_students')


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
