from django.views.generic import DetailView, View
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import *
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.mail import mail_admins, send_mail,EmailMessage
from django.core.files.storage import FileSystemStorage
import datetime
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import UpdateView, DeleteView 
from .forms import LoginForm
# , CourseCreateForm, CourseContentCreateForm, HomeWorkForm,  RegistrationForm
from django.urls import reverse_lazy
import pandas as pd
import random

from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status

class MainPage(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.INFO, 'Please, log in')
            return HttpResponseRedirect('/')
        category = Category.objects.all()
        user = request.user
        last_courses = Course.objects.all().order_by('-pk')[:4]
        template = 'eduapp/main-student.html'
        if user.is_authenticated:
            if user.aps.type == 'teacher':
                last_courses = Course.objects.filter(creator=user.aps)
                template = 'eduapp/main.html'
        context = {
            'categories':category,
            'lastcourses':last_courses
        }
        return render(request, template, context)

# class RegistrationView(View):
#     def get(self, request, *args, **kwargs):
#         form = RegistrationForm(request.POST or None)
#         context = {
#             'form': form,
#         }
#         return render(request, 'eduapp/signup.html', context)

#     def post(self, request, *args, **kwargs):
#         form = RegistrationForm(request.POST,request.FILES or None)
#         if form.is_valid():
#             new_user = form.save(commit=False)
#             new_user.username = form.cleaned_data['username']
#             new_user.email = form.cleaned_data['email']
#             new_user.first_name = form.cleaned_data['first_name']
#             new_user.last_name = form.cleaned_data['last_name']
#             new_user.save()
#             new_user.set_password(form.cleaned_data['password'])
#             new_user.save()
#             AppUser.objects.create(
#                 user=new_user,
#                 avatar=request.FILES['avatar'],
#                 type=form.cleaned_data['type']
#             )
#             user = authenticate(
#                 username=new_user.username, password=form.cleaned_data['password']
#             )
#             login(request, user)
#             messages.add_message(request, messages.SUCCESS, 'Жүйеге сәтті тіркелдіңіз')
#             return HttpResponseRedirect('/')
#         else:
#             print(form.errors)
#         context = {
#             'form': form,
#         }
#         return render(request, 'eduapp/signup.html', context)

class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form,
        }
        return render(request, 'eduapp/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(
                username=username, password=password
            )
            if user:
                login(request, user)
                print(user)
                return HttpResponseRedirect('/main')
        context = {
            'form': form,
        }
        return render(request, 'eduapp/login.html', context)

# class CreateCourse(View):
#     def get(self, request, *args, **kwargs):
#         form = CourseCreateForm(request.POST or None)
#         context = {
#             'form': form,
#         }
#         return render(request, 'eduapp/create-course.html', context)
#     def post(self, request, *args, **kwargs):
#         form = CourseCreateForm(request.POST,request.FILES or None)
#         user = AppUser.objects.get(user=request.user)
#         if form.is_valid():
#             new_course = form.save(commit=False)
#             new_course.creator = user
#             new_course.save()
#         context = {
#             'form': form,
#         }
#         messages.add_message(request, messages.SUCCESS, 'Жаңа курс жүйеге сәтті қосылды')
#         return HttpResponseRedirect('/')

# class TeachersCourse(View):
#     def get(self, request, *args, **kwargs):
#         user = AppUser.objects.get(user=request.user)
#         courses = Course.objects.filter(creator=user)
#         context = {
#             'courses': courses,
#         }
#         return render(request, 'eduapp/teacher-course.html', context)

class StudentsCourse(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.INFO, 'Please, log in')
            return HttpResponseRedirect('/')
        user = AppUser.objects.get(user=request.user)
        
        print(AdmissionCourse.objects.filter(owner=user).first())
        courses = AdmissionCourse.objects.filter(owner=user).first()
        admission = 'asdsda'
        context = {
            'courses': courses,
        }
        return render(request, 'eduapp/student-course.html', context)

# class TeachersCourseDetail(View):
#     def get(self, request, *args, **kwargs):
#         form = CourseContentCreateForm()
#         user = AppUser.objects.get(user=request.user)
#         course_pk = kwargs.get('pk')
#         course = Course.objects.get(creator=user, pk = course_pk)
#         child_courses = CourseContent.objects.filter(course=course).order_by('-priority').reverse()
#         tests = ParentTest.objects.filter(course = course)
#         results = TestResult.objects.filter(test__course=course)  
#         context = {
#             'course': course,
#             'form':form,
#             'courses':child_courses,
#             'tests':tests,
#             'results':results
#         }
#         return render(request, 'eduapp/teacher-course-detail.html', context)

    # def post(self, request, *args, **kwargs):
    #     form = CourseContentCreateForm(request.POST,request.FILES or None)
    #     user = AppUser.objects.get(user=request.user)
    #     course_pk = kwargs.get('pk')
    #     course = Course.objects.get(creator=user, pk = course_pk)
    #     if form.is_valid():
    #         new_course_content = form.save(commit=False)
    #         new_course_content.course=course
    #         new_course_content.save()
    #         course_chat = Chat.objects.create(
    #             course = new_course_content
    #         )
    #     context = {
    #         'course': course,
    #         'form':form
    #     }
    #     messages.add_message(request, messages.SUCCESS, 'Жаңа сабақ жүйеге сәтті қосылды')
    #     return HttpResponseRedirect('/course-list/'+str(course_pk)+'/')

# @csrf_exempt
# def ViewChat(request,pk):
#     if request.method == "GET":
#         course = CourseContent.objects.get(pk=pk)
#         chat = Chat.objects.get(course=course)
#         chat_id = chat.pk
#         messages = Message.objects.filter(chat=chat)
#         chat = ChatSerializer(messages, many=True)
#         data = {
#             'data':chat.data,
#             'chat':chat_id
#         }
#         return JsonResponse(data, safe=True)
#     if request.method == 'POST':
#         print('pp')
# @csrf_exempt
# def AddComment(request):
#     if request.method == 'POST':
#         data = JSONParser().parse(request)
#         chat = data['chat']
#         message = data['message']
#         user = AppUser.objects.get(user=request.user)
#         comment_chat = Chat.objects.get(pk=chat)
#         mes = Message.objects.create(
#             chat = comment_chat,
#             user = user,
#             message = message
#         )
#         if mes:
#             return JsonResponse(data, status=200)

# class CourseContentUpdate(UpdateView):
#     model = CourseContent 
#     fields = [ 
#         "title", 
#         "text",
#         "document",
#         'video',
#         'homework',
#         'priority'
#     ]
#     def get_success_url(self):
#         return reverse_lazy('edu-app:TeachersCourseDetail', kwargs={'pk': self.object.course.pk})
# class CourseContentDelete(DeleteView):
#     model = CourseContent

#     def get_success_url(self):
#         return reverse_lazy('edu-app:TeachersCourseDetail', kwargs={'pk': self.object.course.pk})
class CourseDetail(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.INFO, 'Please, log in')
            return HttpResponseRedirect('/signin/')
        user = AppUser.objects.get(user=request.user)
        course_pk = kwargs.get('pk')
        course = CourseContent.objects.get( pk = course_pk)
      
        context = {
            'course': course,
            'site-user':user,
        }
        return render(request, 'eduapp/course-content-detail.html', context)
    # def post(self, request, *args, **kwargs):
    #     user = AppUser.objects.get(user=request.user)
    #     course_pk = kwargs.get('pk')
    #     course = CourseContent.objects.get( pk = course_pk)
    #     form = HomeWorkForm(request.POST,request.FILES or None)
    #     if form.is_valid():
    #         new_home_w = form.save(commit=False)
    #         new_home_w.student = user
    #         new_home_w.title = form.cleaned_data['title']
    #         new_home_w.course_content = course
    #         new_home_w.file = form.cleaned_data['file']
    #         new_home_w.save()
    #     messages.add_message(request, messages.SUCCESS, 'Үй жұмысы қабылданды')
    #     return HttpResponseRedirect('/course/'+str(course_pk)+'/')

# class CourseDetailContent(View):
#     def get(self, request, *args, **kwargs):
#         user = AppUser.objects.get(user=request.user)
#         course_pk = kwargs.get('pk')
#         course = Course.objects.get(creator=user, pk = course_pk)
#         child_courses = CourseContent.objects.filter(course=course).order_by('-priority').reverse()
#         context = {
#             'course': course,
#             'courses':child_courses
#         }
#         return render(request, 'eduapp/course-content-detail.html', context)
class StudentCourseDetail(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.INFO, 'Please, log in')
            return HttpResponseRedirect('/')
        course_pk = kwargs.get('pk')
        course = Course.objects.get(pk = course_pk)
        child_courses = CourseContent.objects.filter(course=course).order_by('-priority').reverse()
        context = {
            'course': course,
            'courses':child_courses,
            'admission': True,
        }
        return render(request, 'eduapp/student-course-detail.html', context)

class LearnStudentCourseDetail(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.INFO, 'Please, log in')
            return HttpResponseRedirect('/')
        course_pk = kwargs.get('pk')
        course = Course.objects.get(pk = course_pk)
        ParentTest.objects.filter(course=course)
        child_courses = CourseContent.objects.filter(course=course).order_by('-priority').reverse()
        tests = ParentTest.objects.filter(course = course)
        context = {
            'course': course,
            'courses':child_courses,
            'admission': False,
            'tests': tests,
        }
        return render(request, 'eduapp/student-course-detail.html', context)
    # def post(self, request,  *args, **kwargs):
    #     user = request.user
    #     print(user)
    #     course_pk = kwargs.get('pk')
    #     course = Course.objects.get(pk=course_pk)
    #     text = 'тақырыбы - '+request.POST['title']+'/nУақыты - '+request.POST['date-time'] + '/nОқушы - '+ str(user.get_full_name()) + '/nПочта - '+ str(user.email)
    #     print(text)
    #     send_mail('Видео сабққа сұраныс',text, user, [course.creator.user.email], fail_silently=False)
    #     return HttpResponseRedirect('/learn-detail-course/'+str(course_pk)+'/')

class AddCourseToLearn(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.INFO, 'Please log in')
            return HttpResponseRedirect('/signin/')
        course_pk = kwargs.get('pk')
        course = Course.objects.get(pk = course_pk)
        user_courses, created = AdmissionCourse.objects.get_or_create(
            owner=AppUser.objects.get(user=request.user)
        )
        user_courses.courses.add(course)
        messages.add_message(request, messages.SUCCESS, 'successfully added to read list')
        return HttpResponseRedirect('/learn-course-list/')
class CourseByCategory(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.INFO, 'Please, log in')
            return HttpResponseRedirect('/')
        category = kwargs.get('pk')
        category = Category.objects.get(pk=category)
        courses = Course.objects.filter(category = category)
        context = {
            'courses': courses,
            'category':category,
        }
        return render(request, 'eduapp/course-by-category.html', context)

# class CreateTest(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'eduapp/create-test.html')
#     def post(self, request, *args, **kwargs):
#         course = Course.objects.get(pk=kwargs.get('pk'))
#         p_test = ParentTest.objects.create(
#             course = course,
#             title = request.POST['test_title']
#         )
#         file = request.FILES['test_file']
#         db = pd.read_excel(file)
#         for i in db.index:
#             question = db['question'][i]
#             variant = list(str(db['variant'][i]).split(','))
#             index = random.randrange(5)
#             correct = variant[0]
#             move = variant[index]
#             variant[index] = correct
#             variant[0]=move
#             TestItem.objects.create(
#                 parent=p_test,
#                 question = question,
#                 variant = variant,
#                 correct = index
#             )
#         messages.add_message(request, messages.SUCCESS, 'Жаңа тест жүйеге сәтті қосылды')
#         return HttpResponseRedirect('/course-list/'+str(course.pk)+'/')

# class TeacherTestDetail(View):
#     def get(self, request, *args, **kwargs):
#         tests = TestItem.objects.filter(parent = ParentTest.objects.get(pk=kwargs.get('pk')))
#         context = {
#             'tests':tests
#         }
#         return render(request, 'eduapp/teacher-test-detail.html', context)
# class StudentTestDetail(View):
#     def get(self, request, *args, **kwargs):
#         test = ParentTest.objects.get(pk=kwargs.get('pk'))
#         tests = TestItem.objects.filter(parent = test)
#         context = {
#             'test':test,
#             'tests':tests
#         }
#         return render(request, 'eduapp/student-past-test.html', context)
#     def post(self, request, *args, **kwargs):
#         test = ParentTest.objects.get(pk=kwargs.get('pk'))
#         tests = TestItem.objects.filter(parent = test)
#         user = AppUser.objects.get(user=request.user)
#         correct_test_ans = 0
#         count = tests.count()
#         for i in tests:
#             if i.correct == int(request.POST[str(i.pk)]):
#                 correct_test_ans += 1
#         mark = round(int(correct_test_ans)/int(count), 2)*100
#         print(mark)
#         check = TestResult.objects.create(
#             test = test,
#             student = user,
#             correct_ans_count = correct_test_ans,
#             mark = mark
#         )
#         messages.add_message(request, messages.SUCCESS, 'Тест сәтті тапсырылды')
#         return HttpResponseRedirect('/test-result/')
        
# class TestResults(View):
#     def get(self, request, *args, **kwargs):
#         user = AppUser.objects.get(user=request.user)
#         results = TestResult.objects.filter(student = user).order_by('-pk').reverse()
#         context = {
#             'results':results
#         }
#         return render(request, 'eduapp/test-result.html', context)

        

    






