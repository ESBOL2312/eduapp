from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'edu-app'
from . import views

urlpatterns = [
    path('main/', views.MainPage.as_view(), name='MainPage'),
    # path('signup/', views.RegistrationView.as_view(), name='SignUp'),
    path('', views.LoginView.as_view(), name='SignIn'),
    path('logout/', LogoutView.as_view(next_page="/"), name='LogOut'),
    # path('createcourse/', views.CreateCourse.as_view(), name='CreateCourse'),
    # path('course-list/', views.TeachersCourse.as_view(), name='TeachersCourse'),
    path('learn-course-list/', views.StudentsCourse.as_view(), name='StudentsCourse'),
    # path('course-list/<int:pk>/', views.TeachersCourseDetail.as_view(), name='TeachersCourseDetail'),
    # path('course/<pk>/update', views.CourseContentUpdate.as_view(), name="ContentUpdate"), 
    # path('course/<pk>/delete/', views.CourseContentDelete.as_view(), name="ContentDelete"),
    path('course/<int:pk>/', views.CourseDetail.as_view(), name="CourseDetail"),
    # path('course/<int:course>/content/<int:content>', views.CourseDetailContent.as_view(), name="CourseDetailContent"),

    path('detail-course/<int:pk>/', views.StudentCourseDetail.as_view(), name='CourseShow'),
    path('learn-detail-course/<int:pk>/', views.LearnStudentCourseDetail.as_view(), name='LearnCourseShow'),

    path('add-course/<int:pk>/', views.AddCourseToLearn.as_view(), name='CourseAdd'),
    path('category/<int:pk>/', views.CourseByCategory.as_view(), name='CourseByCategory'),
    # path('create-test/<int:pk>/', views.CreateTest.as_view(), name='CreateTest'),
    # path('control-test/<int:pk>/', views.TeacherTestDetail.as_view(), name='ControlTest'),
    # path('past-test/<int:pk>/', views.StudentTestDetail.as_view(), name='PastTest'),
    # path('test-result/', views.TestResults.as_view(), name='TestResult'),
    # path('course/<int:pk>/chat', views.ViewChat, name="ViewChat"),
    # path('course/chat/add/', views.AddComment, name="AddComment"),
    path('ckeditor', include('ckeditor_uploader.urls'))
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)