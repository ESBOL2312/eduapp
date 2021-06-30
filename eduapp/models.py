from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from django.db.models.signals import post_save
from django.dispatch import receiver

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.postgres.fields import ArrayField

from django.contrib.postgres.search import SearchVectorField
User = get_user_model()
# Create your models here.

class AppUser(models.Model):
    user = models.OneToOneField(User, verbose_name='User', on_delete=models.CASCADE, related_name="aps")
    avatar = models.ImageField(upload_to="useravatars/" ,verbose_name="User avatar", blank="true")
    CHOICES = (
        ('student', 'User'),
    )
    type = models.CharField(max_length=100, choices = CHOICES)
    courses = models.ManyToManyField('Course', blank=True, verbose_name='Users spaces', related_name='related_course')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = ("User")
        verbose_name_plural = 'Users'


class Course(models.Model):
    creator = models.ForeignKey(AppUser, verbose_name='Creator', on_delete=models.CASCADE)
    title = models.CharField(max_length=300,verbose_name='Title')
    description = RichTextUploadingField(verbose_name='Description')
    category = models.ForeignKey('Category', verbose_name='Select space', on_delete=models.CASCADE)
    cover =  models.ImageField(upload_to="course/" ,verbose_name="Content poster", blank="true")
    aim = RichTextUploadingField(verbose_name='', blank=True)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = ("Space content")
        # verbose_name_plural = 'Курстар'

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Space name")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = ("Space")
        verbose_name_plural = 'Spaces'


class CourseContent(models.Model):
    course = models.ForeignKey('Course', related_name='Parent_course', on_delete=models.CASCADE,verbose_name="Select space")
    title = models.CharField(max_length=300, verbose_name="Title")
    text = RichTextUploadingField(verbose_name='Description', blank="true")
    video = models.FileField(upload_to="course-video/" ,verbose_name="Video", blank=True,null=True)
    priority = models.IntegerField(verbose_name="Order", blank=True,null=True)
    document = models.FileField(verbose_name="Attach file", blank=True, null="True")
    homework = RichTextUploadingField(verbose_name='additional information', blank=True, null=True)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = ("Content list")
        verbose_name_plural = 'Content lists'

class AdmissionCourse(models.Model):
    owner = models.ForeignKey('AppUser', related_name='Қолданушы', on_delete=models.CASCADE)
    courses = models.ManyToManyField('Course', verbose_name='Қолданушының курстары', blank=True, related_name='user_courses')

# class ParentTest(models.Model):
#     course = models.ForeignKey('Course', related_name='Course_test', on_delete=models.CASCADE)
#     title = models.CharField(max_length=400, default="Курс бойынша тест")
# class TestItem(models.Model):
#     parent = models.ForeignKey('ParentTest', related_name='parent', on_delete=models.CASCADE)
#     question = models.CharField(max_length=400)
#     variant = ArrayField(models.CharField(max_length=800))
#     correct = models.IntegerField()
# class TestResult(models.Model):
#     test = models.ForeignKey('ParentTest', related_name="test", on_delete=models.CASCADE)
#     correct_ans_count = models.IntegerField()
#     student = models.ForeignKey('AppUser', related_name="testable", on_delete=models.CASCADE)
#     mark = models.CharField(max_length=10)
    
# class HomeWork(models.Model):
#     student = models.ForeignKey('AppUser', related_name='sender', on_delete=models.CASCADE)
#     course_content = models.ForeignKey('CourseContent', related_name='subject', on_delete=models.CASCADE)
#     title = models.CharField(max_length=3000, verbose_name='Тақырып')
#     file = models.FileField(upload_to="homeworks/", verbose_name='Файл')
#     sended_data = models.DateTimeField(auto_now=True, verbose_name='Жіберілген күні')

# class Chat(models.Model):
#     course = models.ForeignKey('CourseContent', related_name='parent_course', on_delete=models.CASCADE)
# class Message(models.Model):
#     chat = models.ForeignKey('Chat', related_name='room', on_delete=models.CASCADE)
#     user = models.ForeignKey('AppUser', related_name='meessage_sender', on_delete=models.CASCADE)
#     message = models.TextField()
#     sended_data = models.DateTimeField(auto_now=True, verbose_name='Жіберілген күні')





