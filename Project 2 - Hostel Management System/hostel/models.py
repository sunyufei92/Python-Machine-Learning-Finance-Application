import datetime
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Rooms(models.Model):
    ROOM_TYPES = (
        ('s', "Sports Room"),
        ('l', "Laundry Room"),
    )
    type = models.CharField(max_length=10, null=True, choices=ROOM_TYPES)
    room_no = models.CharField(max_length=100, null=True)
    posting_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room no #{self.room_no}"


class Userregistration(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    regNo = models.IntegerField(null=True)
    gender = models.CharField(max_length=50, null=True)
    contactNo = models.CharField(max_length=15, null=True)
    regDate = models.DateField(null=True)
    updationDate = models.DateTimeField(auto_now_add=True)


class Registration(models.Model):
    rooms = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    regNo = models.CharField(max_length=50, null=True)
    stayfrom = models.CharField(max_length=50, null=True)
    duration = models.CharField(max_length=50, null=True)
    userreg = models.ForeignKey(Userregistration, on_delete=models.CASCADE)
    egycontactno = models.CharField(max_length=15, null=True)
    time_booked = models.DateTimeField(auto_now=True)
    postingDate = models.DateField(null=True, auto_now_add=True)
    updationDate = models.DateField(null=True, auto_now=True)

    @staticmethod
    def get_active_booking(userreg):
        current_time = datetime.datetime.now()
        active_regs = []
        for reg in Registration.objects.filter(userreg=userreg):
            time_passed = current_time - reg.time_booked
            if not time_passed > datetime.timedelta(hours=1):
                active_regs.append(reg)
        return active_regs
