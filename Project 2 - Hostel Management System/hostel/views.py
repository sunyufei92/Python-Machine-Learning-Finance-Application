from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.contrib.auth import login, logout, authenticate
from datetime import date
from django.db.models import Max, Q


# Create your views here.

def index(request):
    regno = 1001 if Userregistration.objects.count() == 0 else Userregistration.objects.aggregate(max=Max('regNo'))[
                                                                   "max"] + 1
    error = ""
    if request.method == 'POST':

        fn = request.POST['firstName']
        ln = request.POST['lastName']
        gen = request.POST['gender']
        cno = request.POST['contactNo']
        e = request.POST['email']
        pas = request.POST['password']

        try:
            user = User.objects.create_user(username=e, password=pas, first_name=fn, last_name=ln)
            Userregistration.objects.create(users=user, regNo=regno, gender=gen, contactNo=cno,
                                            regDate=date.today())
            error = "no"
        except:
            error = "yes"
    return render(request, 'index.html', locals())


def user_login(request):
    error = ""
    if request.method == 'POST':
        e = request.POST['email']
        p = request.POST['pwd']
        user = authenticate(username=e, password=p)
        try:
            if user:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    return render(request, 'user_login.html', locals())


def user_home(request):
    return render(request, 'user_home.html')


def book_Hostel(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    rooms = Rooms.objects.all()
    user = User.objects.get(id=request.user.id)
    userreg, created = Userregistration.objects.get_or_create(users=user)
    regcount = len(Registration.get_active_booking(userreg=userreg))

    if request.method == "POST":
        print(request.POST)
        room_id = request.POST.get("rooms", None)
        room = get_object_or_404(Rooms, id=room_id)

        regNo = request.POST.get("regNo", None)
        firstName = request.POST.get("firstName", None)
        lastName = request.POST.get("lastName", None)
        gender = request.POST.get("gender", None)
        contactNo = request.POST.get("contactNo", None)
        email = request.POST.get("email", None)
        stayfrom = request.POST.get("stayfrom", None)
        duration = request.POST.get("duration", None)
        egycontactno = request.POST.get("egycontactno", None)

        try:
            Registration.objects.create(
                rooms=room,
                regNo=regNo,
                stayfrom=stayfrom,
                duration=duration,
                userreg=userreg,
                egycontactno=egycontactno,
            )
            error = "no"
        except:
            error = "yes"
    return render(request, 'book_Hostel.html', locals())


def room_Details(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user = request.user
    userreg = Userregistration.objects.get(users=user)
    roomdata = Registration.get_active_booking(userreg=userreg)
    return render(request, 'room_Details.html', locals())


def delete_RoomDtls(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    roomdata = Registration.objects.get(id=pid)
    roomdata.delete()
    return redirect('room_Details')


def view_RoomDtls(request, pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    roomdata = Registration.objects.get(id=pid)
    return render(request, 'view_RoomDtls.html', locals())


def my_Profile(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user = User.objects.get(id=request.user.id)
    data = Userregistration.objects.get(users=user)
    return render(request, 'my_Profile.html', locals())


def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user = User.objects.get(id=request.user.id)
    userdata = Userregistration.objects.get(users=user)

    error = ""
    if request.method == "POST":
        rno = request.POST['regNo']
        fname = request.POST['firstName']
        lname = request.POST['lastName']
        gen = request.POST['gender']
        cno = request.POST['contactNo']

        if not rno or rno == "None":
            rno = 000
        userdata.regNo = rno
        userdata.users.first_name = fname
        userdata.users.last_name = lname
        userdata.gender = gen
        userdata.contactNo = cno

        try:
            userdata.save()
            userdata.users.save()
            error = "no"
        except:
            error = "yes"

    return render(request, 'edit_profile.html', locals())


def change_UserPassword(request):
    if not request.user.is_authenticated:
        return redirect('index')
    error = ""
    user = request.user
    if request.method == "POST":
        o = request.POST['old']
        n = request.POST['new']
        try:
            u = User.objects.get(id=request.user.id)
            if user.check_password(o):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = 'not'
        except:
            error = "yes"
    return render(request, 'change_UserPassword.html', locals())


def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    return render(request, 'admin_login.html', locals())


def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    allstudent = Registration.objects.all().count()
    allrms = Rooms.objects.all().count()

    return render(request, 'admin_home.html', locals())


def add_Room(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method == "POST":
        type = request.POST['type']
        rno = request.POST['room_no']
        try:
            Rooms.objects.create(type=type, room_no=rno)
            error = "no"
        except:
            error = "yes"
    return render(request, 'add_Room.html', locals())


def manage_Room(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    room = Rooms.objects.all()
    return render(request, 'manage_Room.html', locals())


def edit_Room(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    room = Rooms.objects.get(id=pid)
    if request.method == "POST":
        type = request.POST['type']
        rno = request.POST['room_no']

        room.room_no = rno
        room.type = type

        try:
            room.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'edit_Room.html', locals())


def delete_Room(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    room = Rooms.objects.get(id=pid)
    room.delete()
    return redirect('manage_Room')


def student_Registration(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    rooms = Rooms.objects.all()
    regno = 1001 if Userregistration.objects.count() == 0 else Userregistration.objects.aggregate(max=Max('regNo'))[
                                                                   "max"] + 1
    if request.method == 'POST':
        rid = request.POST['rooms']
        room = Rooms.objects.get(id=rid)

        stayfrom = request.POST['stayfrom']
        duration = request.POST['duration']

        fn = request.POST['firstName']
        ln = request.POST['lastName']
        gen = request.POST['gender']
        cno = request.POST['contactNo']
        e = request.POST['email']
        pas = request.POST['password']
        egycontactno = request.POST['egycontactno']

        # try:
        user, created = User.objects.get_or_create(username=e)
        user.set_password(pas)
        user.first_name = fn
        user.last_name = ln
        user.save()
        userreg, created = Userregistration.objects.get_or_create(users=user)
        userreg.regNo = regno
        userreg.gender = gen
        userreg.contactNo = cno
        userreg.regDate = date.today()
        userreg.save()

        Registration.objects.create(
            rooms=room,
            regNo=regno,
            stayfrom=stayfrom,
            duration=duration,
            userreg=userreg,
            egycontactno=egycontactno,
        )
        error = "no"
        # except:
        #     error = "yes"
    return render(request, 'student_Registration.html', locals())


def manage_student(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    stdata = Registration.objects.all()
    return render(request, 'manage_student.html', locals())


def view_RegistrationDtls(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    roomdata = Registration.objects.get(id=pid)
    return render(request, 'view_RegistrationDtls.html', locals())


def changePassword(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    user = request.user
    if request.method == "POST":
        o = request.POST['oldpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if user.check_password(o):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = 'not'
        except:
            error = "yes"
    return render(request, 'changePassword.html', locals())


def delete_StudentReg(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    roomdata = Registration.objects.get(id=pid)
    roomdata.delete()
    roomdata.userreg.delete()
    roomdata.userreg.users.delete()
    return redirect('manage_student')


def Logout(request):
    logout(request)
    return redirect('index')


def search_students(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    students = User.objects.all()
    if request.method == "POST":
        query = request.POST['query']
        students = User.objects.filter(
            Q(email__icontains=query) | Q(username__icontains=query) | Q(first_name__icontains=query) | Q(
                last_name__icontains=query))
    return render(request, 'students.html', locals())
