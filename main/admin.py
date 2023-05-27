from django.contrib import admin
from accounts.models import Timetable, Subject, Group, UserSubject, MainTest, StudentTest, Task, AnswerTask, Lecture, \
    LectureFile, Practice, Test


class LectureFileInline(admin.TabularInline):
    model = LectureFile
    extra = 0


class TestInline(admin.TabularInline):
    model = Test
    extra = 0


@admin.register(MainTest)
class A(admin.ModelAdmin):
    inlines = [TestInline]
    list_display = ['id', 'subject']


@admin.register(Lecture)
class A(admin.ModelAdmin):
    inlines = [LectureFileInline]


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    filter_horizontal = ['teachers']
    search_fields = ['name']


@admin.register(Subject)
class A(admin.ModelAdmin):
    list_display = ['id', 'name']


admin.site.register(Practice)
admin.site.register(Timetable)
admin.site.register(Task)
admin.site.register(AnswerTask)
admin.site.register(StudentTest)
admin.site.register(UserSubject)
