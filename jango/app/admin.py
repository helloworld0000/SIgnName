from django.contrib import admin

# Register your models here.
from app.models import Student,Course,Attendence


class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'student_name', 'get_course1','get_course2','student_grade')  # list

    def get_course1(self, obj):
        return obj.course1.course_name

    get_course1.admin_order_field = 'course'  # Allows column order sorting
    get_course1.short_description = 'course1 Name'  # Renames column head

    def get_course2(self, obj):
        return obj.course2.course_name

    get_course2.admin_order_field = 'course'  # Allows column order sorting
    get_course2.short_description = 'course2 Name'  # Renames column head



class AttendenceAdmin(admin.ModelAdmin):
    list_display = ('get_studentid','get_studentname', 'get_course', 'time','ip')  # list

    def get_studentid(self, obj):
        return obj.student.student_id

    get_studentid.admin_order_field = 'student'  # Allows column order sorting
    get_studentid.short_description = 'studentid'  # Renames column head

    def get_studentname(self, obj):
        return obj.student.student_name

    get_studentname.admin_order_field = 'student'  # Allows column order sorting
    get_studentname.short_description = 'studentname'  # Renames column head

    def get_course(self, obj):
        return obj.course.course_name

    get_course.admin_order_field = 'course'  # Allows column order sorting
    get_course.short_description = 'course Name'  # Renames column head



admin.site.register(Student,StudentAdmin)
admin.site.register(Course)
admin.site.register(Attendence,AttendenceAdmin)

