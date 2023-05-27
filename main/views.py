from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.models import Timetable, MainTest, Subject, UserSubject, UserAbsence, Task, AnswerTask, Test, \
    StudentTest, Lecture, Practice
from .serializers import SubjectSerializer, UserSubjectSerializer, UserAbsenceSerializer, GroupSerializer, \
    MainTestSerializer, TaskSerializer, TestSerializer, MainTestListSerializer, StudentTaskSerializer, \
    LectureSerializer, PracticeSerializer, TaskListSerializer


class LectureView(generics.ListAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer

    def get_queryset(self):
        return self.queryset.filter(subject_id=self.kwargs.get('pk'))


class PracticeView(generics.ListAPIView):
    queryset = Practice.objects.all()
    serializer_class = PracticeSerializer

    def get_queryset(self):
        return self.queryset.filter(subject_id=self.kwargs.get('pk'))


class AnswerTestView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        test_id = self.request.data['test_id']
        score = self.request.data['score']
        StudentTest.objects.create(user=user, test_id=test_id, score=score)
        return Response({'success': True}, status=status.HTTP_201_CREATED)


class AnswerTaskCreateView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        task_id = self.request.data['task_id']
        file = self.request.data['file']
        AnswerTask.objects.create(user=user, file=file, task_id=task_id)
        return Response({'success': True}, status=status.HTTP_201_CREATED)


class TaskCreateView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        data = self.request.data
        if user.subject:
            data['subject'] = user.subject.id
            serializer = TaskSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'success': True}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'message': 'You has not subject'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class MainTestListAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        ls = list()
        ans_test = list()
        user = self.request.user
        if user.group:
            group = user.group
            for i in StudentTest.objects.filter(user=user):
                ans_test.append(i.test.id)
            qs = MainTest.objects.filter(group_id=group.id)
            for i in qs:
                data = MainTestListSerializer(instance=i).data
                if data['id'] in ans_test:
                    obj = StudentTest.objects.filter(test_id=data['id']).first()
                    data['score'] = obj.score
                    data['is_completed'] = True
                else:
                    data['score'] = None
                    data['is_completed'] = False
                ls.append(data)
        return Response(ls)


class StudentTestView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        ls = list()
        qs = Test.objects.filter(test_id=self.kwargs.get('pk'))
        for i in qs:
            ls.append(TestSerializer(instance=i).data)
        return Response(ls)


class MainTestCreateAPIView(generics.GenericAPIView):
    serializer_class = MainTestSerializer
    queryset = MainTest.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        sub = user.subject
        data = self.request.data
        data['subject'] = sub.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TestCreateView(generics.CreateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class GroupListAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        ls = list()
        for i in user.my_groups.all():
            ls.append(GroupSerializer(instance=i).data)
        return Response(ls)


class GroupDetailView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        ls = list()
        user = self.request.user
        if user.subject:
            qs = Task.objects.filter(subject_id=user.subject.id, group_id=self.kwargs.get('pk'))
            for i in qs:
                ls.append(TaskListSerializer(instance=i).data)
        return Response(ls)


class MarkView(views.APIView):
    def patch(self, request, *args, **kwargs):
        obj = AnswerTask.objects.filter(id=self.kwargs.get('pk')).first()
        obj.mark = self.request.data['mark']
        obj.save()
        return Response({'success': True})


class TimeTableAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.group:
            obj = Timetable.objects.filter(group_id=user.group.id).first()
            path = obj.file_path
        else:
            path = None
        return Response({'file': path})


class SubjectListAPIView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        ls = list()
        subject_ids_ls = list()
        for i in UserSubject.objects.filter(user=self.request.user):
            subject_ids_ls.append(i.subject.id)
        for i in self.queryset.all():
            data = self.get_serializer(instance=i).data
            data['nb'] = UserAbsence.objects.filter(user=self.request.user, subject_id=i.id).count()
            if i.id in subject_ids_ls:
                data['selected'] = True
            else:
                data['selected'] = False
            ls.append(data)
        return Response(ls)


class SubjectDetailView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        ls = list()
        user = self.request.user
        score = 0
        max_score = 0
        percent = 0
        current_mark = 0
        if user.group:
            user_sb = UserSubject.objects.get(id=self.kwargs.get('pk'))
            qs = Task.objects.filter(subject_id=user_sb.subject.id, group_id=user.group.id)
            for i in qs:
                data = StudentTaskSerializer(instance=i).data
                obj = AnswerTask.objects.filter(user=user, task_id=i.id).first()
                if obj:
                    data['answer_file'] = obj.file_path
                    data['mark'] = obj.mark
                    if obj.mark:
                        score += obj.mark
                    else:
                        score += 0
                else:
                    data['answer_file'] = None
                    data['mark'] = None
                ls.append(data)
            max_score = sum([i.max_mark for i in qs])
            if max_score == 0:
                max_score = 1
            percent = round((score * 100) / max_score)
            if percent <= 56:
                current_mark = 2
            elif (percent > 56) and (percent < 70):
                current_mark = 3
            elif (percent >= 70) and (percent <= 85):
                current_mark = 4
            elif percent > 85:
                current_mark = 5
            return Response(
                {'current_mark': current_mark, 'max_score': max_score, 'percent': percent, 'score': score, 'tasks': ls})
        return Response(
            {'current_mark': current_mark, 'max_score': max_score, 'percent': percent, 'score': score, 'tasks': []})


class TeacherTimeTableView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        obj = Subject.objects.filter(teacher=user).first()
        return Response({'file': obj.file_path})


class TakeSubjectAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        sb = Subject.objects.filter(id=self.request.data['subject_id']).first()
        UserSubject.objects.create(user=self.request.user, subject=sb)
        return Response({'success': True}, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        sb = Subject.objects.filter(id=self.request.data['subject_id']).first()
        UserSubject.objects.filter(user=self.request.user, subject=sb).delete()
        return Response({'success': True})

    def get(self, request, *args, **kwargs):
        qs = UserSubject.objects.filter(user=self.request.user)
        serializer = UserSubjectSerializer(qs, many=True)
        return Response(serializer.data)


class UserAbsenceListAPIView(generics.ListAPIView):
    serializer_class = UserAbsenceSerializer

    def get_queryset(self):
        queryset = UserAbsence.objects.filter(user=self.request.user)
        return queryset
