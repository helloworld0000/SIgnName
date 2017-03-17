from django.contrib import admin

# Register your models here.
from app.models import Student,Course,Attendence

admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Attendence)

