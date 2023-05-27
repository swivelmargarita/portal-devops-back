from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **kwargs):
        if not phone:
            raise TypeError('Invalid phone number')
        user = self.model(phone=phone, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **kwargs):
        if not password:
            raise TypeError('password no')
        user = self.create_user(phone, password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class Group(models.Model):
    name = models.CharField(max_length=250)
    teachers = models.ManyToManyField('User', limit_choices_to={'role': 'Teacher'}, related_name='my_groups',
                                      blank=True)

    def __str__(self):
        return self.name

    @property
    def get_count(self):
        return self.members.count()


class User(AbstractBaseUser, PermissionsMixin):
    ROLE = (
        ("Teacher", "Teacher"),
        ("Student", "Student")
    )
    name = models.CharField(max_length=350)
    last_name = models.CharField(max_length=132, null=True, blank=True)
    phone = models.CharField(max_length=13, unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    role = models.CharField(choices=ROLE, max_length=20, default='Student')
    group = models.ForeignKey(Group, models.SET_NULL, null=True, blank=True, related_name='members')

    objects = UserManager()
    USERNAME_FIELD = 'phone'

    def __str__(self):
        return self.phone


class Subject(models.Model):
    name = models.CharField(max_length=223)
    file = models.FileField(upload_to='subject_timetables')
    teacher = models.OneToOneField(User, models.SET_NULL, null=True, blank=True, related_name='subject',
                                   limit_choices_to={'role': 'Teacher'})

    def __str__(self):
        return self.name

    @property
    def file_path(self):
        return f"{settings.SITE_URL}{self.file.url}"


class Lecture(models.Model):
    subject = models.ForeignKey(Subject, models.CASCADE)
    theme = models.CharField(max_length=250)
    date = models.DateField()


class LectureFile(models.Model):
    lecture = models.ForeignKey(Lecture, models.CASCADE, related_name='files')
    file = models.FileField(upload_to='lecture_files')

    @property
    def file_path(self):
        return f"{settings.SITE_URL}{self.file.url}"


class Practice(models.Model):
    subject = models.ForeignKey(Subject, models.CASCADE)
    theme = models.CharField(max_length=250)
    date = models.DateField()


class VerifyPhone(models.Model):
    phone = models.CharField(max_length=15, verbose_name="Verify Phone")
    code = models.CharField(max_length=10, verbose_name="Code")

    def __str__(self):
        return self.phone


class Timetable(models.Model):
    group = models.OneToOneField(Group, models.CASCADE)
    name = models.CharField(max_length=123)
    file = models.FileField(upload_to='files/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def file_path(self):
        return f"{settings.SITE_URL}{self.file.url}"


class MainTest(models.Model):
    group = models.ForeignKey(Group, models.CASCADE, related_name='tests')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='tests')
    start_time = models.DateTimeField()
    max_mark = models.PositiveIntegerField()
    type = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.subject.name


class Test(models.Model):
    test = models.ForeignKey(MainTest, models.CASCADE)
    question_name = models.TextField()
    answer_a = models.CharField(max_length=223)
    answer_b = models.CharField(max_length=223)
    answer_c = models.CharField(max_length=223)
    answer_d = models.CharField(max_length=223)
    answer_true = models.CharField(max_length=223)

    def __str__(self):
        return self.question_name


class StudentTest(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name='tests')
    test = models.OneToOneField(MainTest, models.CASCADE, related_name='tests')
    score = models.FloatField()

    def __str__(self):
        return f"{self.user.name} {self.test.subject}"


class Task(models.Model):
    title = models.CharField(max_length=250)
    group = models.ForeignKey(Group, models.CASCADE, related_name='tasks')
    subject = models.ForeignKey(Subject, models.CASCADE)
    file = models.FileField(upload_to='subject_tasks')
    deadline = models.DateTimeField()
    max_mark = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.group.name

    @property
    def file_path(self):
        return f"{settings.SITE_URL}{self.file.url}"


class AnswerTask(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    task = models.ForeignKey(Task, models.CASCADE, related_name='answers')
    file = models.FileField(upload_to='answer_files')
    mark = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task.subject.name

    @property
    def file_path(self):
        return f"{settings.SITE_URL}{self.file.url}"


class UserSubject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='user_subjects')

    def __str__(self):
        return self.user.phone


class UserAbsence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_absences')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='user_absences')
    count_nb = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.phone
