from accounts.models import Group, MainTest, Subject, UserSubject, UserAbsence, Task, Test, Practice, Lecture, \
    LectureFile, AnswerTask
from rest_framework import serializers


class LectureFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureFile
        fields = ['file_path']


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['theme', 'date', 'files']

    files = LectureFileSerializer(many=True)


class PracticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Practice
        fields = ['theme', 'date']


class AnswerTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerTask
        fields = ['id', 'user', 'file_path', 'created_at', 'mark']

    user = serializers.SerializerMethodField()

    @staticmethod
    def get_user(obj):
        return f"{obj.user.name} {obj.user.last_name}"


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'max_mark', 'deadline', 'file_path', 'answers']

    answers = AnswerTaskSerializer(many=True)


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['group', 'title', 'subject', 'file', 'deadline', 'max_mark']
        extra_kwargs = {
            'subject': {'required': False}
        }


class StudentTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'file_path', 'deadline', 'max_mark', 'teacher', 'title']

    teacher = serializers.SerializerMethodField()

    @staticmethod
    def get_teacher(obj):
        if obj.subject.teacher:
            return f"{obj.subject.teacher.name} {obj.subject.teacher.last_name}"
        return 'Has not teacher'


class MainTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainTest
        fields = ['id', 'group', 'start_time', 'max_mark', 'subject', 'type']
        extra_kwargs = {
            'subject': {'required': False}
        }

    id = serializers.IntegerField(read_only=True)


class MainTestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainTest
        fields = ['id', 'date', 'time', 'max_mark', 'subject', 'teacher', 'type']

    subject = serializers.CharField(source='subject.name')
    date = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    teacher = serializers.SerializerMethodField()

    @staticmethod
    def get_teacher(obj):
        if obj.subject.teacher:
            return f"{obj.subject.teacher.name} {obj.subject.teacher.last_name}"
        return 'Has not teacher'

    @staticmethod
    def get_date(obj):
        return obj.start_time.strftime('%d-%m-%Y')

    @staticmethod
    def get_time(obj):
        return obj.start_time.strftime('%-H:%M')


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['test', 'answer_true', 'question_name', 'answer_a', 'answer_b', 'answer_c', 'answer_d']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'get_count']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'teacher_full_name']

    teacher_full_name = serializers.SerializerMethodField()

    @staticmethod
    def get_teacher_full_name(obj):
        if obj.teacher:
            return f"{obj.teacher.name} {obj.teacher.last_name}"
        return 'Has not teacher'


class UserSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubject
        fields = ['id', 'subject_id', 'name', 'teacher_full_name', 'count_nb']

    name = serializers.CharField(source='subject.name')
    subject_id = serializers.IntegerField(source='subject.id')
    teacher_full_name = serializers.SerializerMethodField()
    count_nb = serializers.SerializerMethodField()

    @staticmethod
    def get_teacher_full_name(obj):
        if obj.subject.teacher:
            return f"{obj.subject.teacher.name} {obj.subject.teacher.last_name}"
        return 'Has not teacher'

    @staticmethod
    def get_count_nb(obj):
        if obj.user.user_absences.first():
            return sum([i.count_nb for i in obj.user.user_absences.all()])
        return 0


class UserAbsenceSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()

    class Meta:
        model = UserAbsence
        fields = ['id', 'subject', 'count_nb']
