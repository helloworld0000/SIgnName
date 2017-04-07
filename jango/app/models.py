from django.db import models
from django import forms

# Create your models here.


class Artist(models.Model):#from the model class!
    id = models.AutoField(primary_key=True)
    name = models.CharField("artist",max_length=50)
    created_date = models.DateField("date",auto_now_add=True)


class Alum(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("alum",max_length=50)
    artist = models.ForeignKey(Artist)

class Course(models.Model):

    id = models.AutoField(primary_key=True)
    course_id = models.CharField("course_id",max_length=50)
    course_name = models.CharField("course_name",max_length=50)
    course_begintime = models.TimeField('%H:%M','course_begintime')
    course_endtime = models.TimeField('%H:%M','course_endtime')
    course_semester = models.CharField("course_semester",default='0',max_length=5)

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.CharField("student_id", max_length=10)
    student_name = models.CharField("student_name",max_length=50)
    student_password = models.CharField("student_password", max_length=50)
    course1 = models.ForeignKey(Course,related_name="firstcourse")
    course2 = models.ForeignKey(Course,related_name="secondcourse")
    student_grade = models.CharField("student_grade",max_length=50)
    attendence = models.ManyToManyField(Course, through='Attendence',related_name='Attendence')

class Attendence(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student,related_name='student')
    course = models.ForeignKey(Course,related_name='course')
    time = models.DateTimeField('time',"time",auto_now_add=True)
    ip = models.CharField("ip",max_length=20,default='192.168.7.1')


# class User(models.Model):
#     student = models.ForeignKey(Student,related_name="student")
#     password = models.TextField(null=False,max_length=20)
#     class Meta:
#         db_table = 'user'






