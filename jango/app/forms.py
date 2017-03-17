#-*- coding: utf-8 -*-

from django.forms import ModelForm
from django import forms

from app.models import Student,Attendence,Artist,Alum,Course

class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='',
        error_messages={'required': '请输入学号'},
        widget=forms.TextInput(
            attrs={
                'placeholder':u"学号",
                'class':"form-control",
            }
        ),
    )
    password = forms.CharField(
        required=True,
        label='',
        error_messages={'required': u'请输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"密码",
                'class': "form-control",
            }
        ),
        )



    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"用户名和密码为必填项")
        else:
            cleaned_data = super(LoginForm, self).clean()



class ArtistForm(ModelForm):
    class Meta:
        model = Artist
        fields = ['name']

class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        # return "%s %s" % (obj.course_name, obj.course_begintime)
        return obj.course_name

class StudentForm(forms.ModelForm):
    # def __init__(self):
    #     super(StudentForm,self).__init__()
    #     self.fields['course1'].queryset = Course.objects.all()
    #     self.fields['course1'].label_from_instance = lambda obj:"%s %s"%(obj.course_name,obj.course_begintime)
    class Meta:
        model = Student
        # fields = ('student_id', 'course1','course2', 'student_grade')
        fields = ('student_id', 'student_name','student_password', 'course1', 'course2', 'student_grade')
    student_id = forms.IntegerField(required=True,widget=forms.TextInput(attrs={'class':'form-group form-control fa fa-user fa-fw'}),label='学号')
    student_name = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-group form-control fa fa-user fa-fw'}),label='姓名')
    student_password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class':'form-group form-control fa fa-user fa-fw'}),label='密码')
    course1 = CustomModelChoiceField(queryset=Course.objects.all(),widget=forms.Select(attrs={'class':'form-group form-control fa fa-user fa-fw'}),label='选择课程1')
    course2 = CustomModelChoiceField(queryset=Course.objects.all(),widget=forms.Select(attrs={'class':'form-group form-control fa fa-user fa-fw'}),label='选择课程2')
    student_grade = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-group form-control fa fa-user fa-fw'}),label='请输入年级（1/2/3）')

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ('course_id','course_name','course_begintime','course_endtime','course_semester')

    course_id = forms.IntegerField(required=True, widget=forms.TextInput(
            attrs={'class': 'form-group form-control fa fa-user fa-fw','placeholder':u"课程编号",}), label='')
    course_name = forms.CharField(required=True, widget=forms.TextInput(
            attrs={'class': 'form-group form-control fa fa-user fa-fw','placeholder':u"课程名称",}), label='')
    course_begintime = forms.TimeField(required=True, widget=forms.TextInput(
            attrs={'class': 'form-group form-control fa fa-user fa-fw','placeholder':u"开始时间",}), label='')
    course_endtime = forms.TimeField(required=True, widget=forms.TextInput(
            attrs={'class': 'form-group form-control fa fa-user fa-fw','placeholder':u"结束时间",}), label='')
    course_semester = forms.CharField(required=True, widget=forms.TextInput(
            attrs={'class': 'form-group form-control fa fa-user fa-fw','placeholder':u"星期几（*周日为0，依次递加）",}), label='')


class AttendenceForm(forms.ModelForm):
    class Meta:
        model = Attendence
        fields = ['course']

    course = CustomModelChoiceField(queryset=Course.objects.all(),widget=forms.Select(attrs={'class': 'form-control'}),label='请选择签到课程')