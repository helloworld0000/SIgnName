#-*- coding: utf-8 -*-


from django.shortcuts import render,render_to_response,HttpResponseRedirect
from django.http import HttpRequest,HttpResponse
from django.template import RequestContext

from app.forms import ArtistForm, CourseForm, StudentForm,LoginForm,AttendenceForm
from app.models import *
from django.views.decorators.csrf import csrf_exempt
import time
import datetime as dt
@csrf_exempt

# Create your views here.

def artists(request):
    # return  HttpResponse('<html><body>Hello!!! DazaMing </body></html>')
    artists = Artist.objects.all()
    return render_to_response('artists.html',{'artists': artists})

def artistdetails(request,id):
    artist = Artist.objects.get(pk=id)
    return render_to_response('artistdetails.html', {'artist': artist})
def createartist(request):
    if request.method == "GET":
        form = ArtistForm()
        return render(request,'createArtists.html',{'form':form})
    if request.method == "POST":
        form = ArtistForm(request.POST)
        form.save()
        return HttpResponseRedirect('/artists')
def courses(request):
    # return  HttpResponse('<html><body>Hello!!! DazaMing </body></html>')
    courses = Course.objects.all()
    return render_to_response('courses.html',{'courses': courses})

def coursedetails(request,id):
    course = Course.objects.get(pk=id)
    return render_to_response('coursedetails.html', {'course': course})

def createcourse(request):
    if request.method == "GET":
        form = CourseForm()
        return render(request,'createCourses.html',{'form':form})
    if request.method == "POST":
        form =CourseForm(request.POST)
        form.save()
        return HttpResponseRedirect('/courses')

def register(request):
    if request.method == 'GET':
        return  render(request,'register.html')
    if request.method == 'POST':
        return render(request, 'register.html')


def students(request):

    if request.method == "GET":
        form = LoginForm()
        return render_to_response('students.html',{'form': form})

    if request.method == "POST":
        form = LoginForm(request.POST)
        attendform = AttendenceForm
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = Student.objects.filter(student_id=username, student_password=password)
            if user:
                userid = user[0].id
                request.session['student_id'] = userid
                print(request.session['student_id'])
                allattendce = Attendence.objects.filter(student=user[0])
                return render_to_response('studentdetails.html',{'student': user[0],'form':attendform,'attendences':allattendce})


            else:

                return render_to_response('students.html',
                                          RequestContext(request, {'form': form, 'password_is_wrong': True}))

        else:
            return render('students.html', RequestContext(request, {'form': form,}))


from datetime import datetime,date

def studentprofile(request):
    if request.method == "GET":
        #return the profile page
        studentid = int(request.session['student_id'])
        student = Student.objects.get(pk=studentid)
        form =  StudentForm(instance= student)

        return render(request, 'Studentprofile.html', {'student': student , 'form':form})

    if request.method == "POST":

        studentid = int(request.session['student_id'])
        student = Student.objects.get(pk=studentid)
        form = StudentForm(request.POST or None, instance=student)
        if form.is_valid():
            form.save()
            allattendce = Attendence.objects.filter(student=student)
            return HttpResponseRedirect('/studentdetails')
        else:
            return render(request, 'Studentprofile.html', {'student': student, 'form': form,'error':True})


from django.utils import timezone


def studentdetails(request):
    if request.method == "GET":
        form = AttendenceForm()
        studentid = int(request.session['student_id'])
        student = Student.objects.get(pk=studentid)
        allattendce = Attendence.objects.filter(student=student)
        return render_to_response('studentdetails.html', RequestContext(request, {'form': form,
                                                                                  'attendences': allattendce,
                                                                                  'student': student}))
    if request.method == "POST":
        form = AttendenceForm(request.POST)
        studentid = int(request.session['student_id'])
        student = Student.objects.get(pk=studentid)
        print(student.student_name)
        allattendce = Attendence.objects.filter(student=student)
        if form.is_valid():

            course = form.cleaned_data['course']
            timenow = time.strftime('%H:%M',time.localtime(time.time()))
            Datenow = time.strftime('%Y-%m-%d',time.localtime(time.time()))
            print(Datenow)
            date = Datenow.split('-')
            now = timezone.now()
            weekday = int(datetime.now().weekday())
            print('weekday'+str(weekday))
            ip = getclientip(request)
            print(ip)

            coursebegintime =course.course_begintime
            coursebegintime = str(coursebegintime)[:5]
            courseendtime =course.course_endtime
            courseendtime = str(courseendtime)[:5]
            coursesemester = int(course.course_semester)

            print(str(timenow))
            print(course.course_semester)
            print(course.course_name)
            print(coursebegintime)
            print(courseendtime)
            print('========================')
            print(date[0]+"aaa"+date[1]+'aaa'+date[2])
            if course.id == 5:
                # checkip = Attendence.objects.filter(ip=ip,time__year=date[0],time__month=date[1],time__day=date[2])
                checkip = Attendence.objects.filter(ip=ip,student=student)
                for eachattendence in checkip:
                    print(str((eachattendence).time))
                    if str((eachattendence).time)[:10] == Datenow:
                        if now-eachattendence.time<dt.timedelta(minutes=30) :
                            return render_to_response('studentdetails.html', RequestContext(request, {'form': form,
                                                                                                  'repeat_is_wrong': True,
                                                                                                  'student': student,
                                                                                                  'attendences': allattendce}))
                attendence = Attendence(student=student, course=course, ip=ip)
                attendence.save()
                return render_to_response('studentdetails.html', RequestContext(request, {'form': form,
                                                                                          'attendences': allattendce,
                                                                                          'student': student}))

            if (int(weekday) == coursesemester) and (str(timenow)<= courseendtime) and (str(timenow)>= coursebegintime):
                #check ip
                checkip = Attendence.objects.filter(ip=ip,course=course)
                for eachattendence in checkip:
                    if str((eachattendence).time)[:10] == Datenow:
                        return render_to_response('studentdetails.html',RequestContext(request, {'form': form, 'ip_is_wrong': True,'student':student,'attendences': allattendce}))


                    # insert the Attendence

                attendence = Attendence(student=student, course=course, ip=ip)
                attendence.save()


                return render_to_response('studentdetails.html', RequestContext(request, {'form':form,'attendences': allattendce,'student':student}))

            else:
                return render_to_response('studentdetails.html',RequestContext(request, {'form': form, 'time_is_wrong': True,'student':student,'attendences': allattendce}))


        else:
            return render('studentsdetails.html', RequestContext(request, {'form': form,'student':student,'attendences': allattendce}))
def getclientip(request):
    ther = request.META.get('HTTP_X_FORWARDED_FOR')
    if ther:
        ip = ther.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
def createstudent(request):
    if request.method == "GET":
        form = StudentForm()
        return render(request,'createStudent.html',{'form':form})

    if request.method == "POST":
        form =StudentForm(request.POST)
        form.save()
        user = Student.objects.filter(student_id=form.cleaned_data['student_id'], student_password=form.cleaned_data['student_password'])
        if user:
            userid = user[0].id
            request.session['student_id'] = userid
        return HttpResponseRedirect('/studentdetails')
def getattendence(grade,week):
    weekcount = [0,0,0,0,0]
    checkattendence1 = Attendence.objects.filter(student__student_grade=grade)
    for attendence1 in checkattendence1:
        for i in range(0,5):
            time = str(attendence1.time)[0:10]
            if time in week[i]:
                weekcount[i] += 1
    return weekcount
def getechartvalues():
    week = []
    echartsvalues = []
    week1 = ['2017-02-27','2017-02-28','2017-03-01','2017-03-02''2017-03-03''2017-03-04' '2017-03-05']
    week2 = ['2017-03-06','2017-03-07','2017-03-08','2017-03-09','2017-03-10','2017-03-11', '2017-03-12']
    week3 = ['2017-03-13','2017-03-14','2017-03-15','2017-03-16','2017-03-17','2017-03-18', '2017-03-19']
    week4 = ['2017-03-20','2017-03-21','2017-03-22','2017-03-23','2017-03-24','2017-03-25', '2017-03-26']
    week5 = ['2017-03-27','2017-03-28','2017-03-29','2017-03-30','2017-03-31','2017-04-01', '2017-04-02']
    week6 = ['2017-04-03', '2017-04-04', '2017-04-05', '2017-04-06', '2017-04-07', '2017-04-08', '2017-04-09']
    week7 = ['2017-04-10', '2017-04-11', '2017-04-12', '2017-04-13', '2017-04-14', '2017-04-15', '2017-04-16']
    week8 = ['2017-04-17', '2017-04-18', '2017-04-19', '2017-04-20', '2017-04-21', '2017-04-22', '2017-04-23']
    week9 = ['2017-04-24', '2017-04-25', '2017-04-26', '2017-04-27', '2017-04-28', '2017-04-29', '2017-04-30']

    week.append(week1)
    week.append(week2)
    week.append(week3)
    week.append(week4)
    week.append(week5)
    week.append(week6)
    week.append(week7)
    week.append(week8)
    week.append(week9)

    echartsvalues1 = getattendence('1',week)
    echartsvalues2 = getattendence('2', week)
    echartsvalues3 = getattendence('3', week)
    echartsvalues.append(echartsvalues1)
    echartsvalues.append(echartsvalues2)
    echartsvalues.append(echartsvalues3)
    return echartsvalues


def index(request):
    echartsvalues = getechartvalues()
    print(echartsvalues[0])
    print(echartsvalues[1])
    print(echartsvalues[2])
    return render_to_response('index.html',RequestContext(request, {'grade1': echartsvalues[0],'grade2': echartsvalues[1],'grade3': echartsvalues[2]}))
    # return render(request,'index.html')

