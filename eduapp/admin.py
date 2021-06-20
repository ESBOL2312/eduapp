from django.contrib import admin

# Register your models here.



from .models import *

# Register your models here.
admin.site.register(AppUser)
admin.site.register(Course)
admin.site.register(Category)
admin.site.register(CourseContent)
admin.site.register(AdmissionCourse)
# admin.site.register(ParentTest)
# admin.site.register(TestItem)
# admin.site.register(HomeWork)
# admin.site.register(Chat)
# admin.site.register(Message)


