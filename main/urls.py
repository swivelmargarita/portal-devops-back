from . import views
from django.urls import path

urlpatterns = [
    path('timetable/', views.TimeTableAPIView.as_view()),
    path('my-test/', views.MainTestListAPIView.as_view()),
    path('my-test/<int:pk>/', views.StudentTestView.as_view()),
    path('test-create/', views.MainTestCreateAPIView.as_view()),
    path('child-test-create/', views.TestCreateView.as_view()),
    path('answer-test/', views.AnswerTestView.as_view()),
    path('my-groups/', views.GroupListAPIView.as_view()),
    path('group/<int:pk>/', views.GroupDetailView.as_view()),
    path('mark-task/<int:pk>/', views.MarkView.as_view()),
    path('teacher-timetable/', views.TeacherTimeTableView.as_view()),
    path('subject-list/', views.SubjectListAPIView.as_view()),
    path('subject/<int:pk>/', views.SubjectDetailView.as_view()),
    path('lecture/<int:pk>/', views.LectureView.as_view()),
    path('practice/<int:pk>/', views.PracticeView.as_view()),
    path('user-subject/', views.TakeSubjectAPIView.as_view()),
    path('user-absence/', views.UserAbsenceListAPIView.as_view()),
    path('task/', views.TaskCreateView.as_view()),
    path('answer-task/', views.AnswerTaskCreateView.as_view()),

]
