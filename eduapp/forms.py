from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import AppUser
# , Course, CourseContent, HomeWork
from ckeditor.widgets import CKEditorWidget

User = get_user_model()

# class RegistrationForm(forms.ModelForm):
#     confirm_password = forms.CharField(widget = forms.PasswordInput)
#     password = forms.CharField(widget = forms.PasswordInput)
#     avatar = forms.FileField(required=False)
#     email = forms.EmailField(required=False)
#     CHOICES = (
#         ('teacher', 'Оқытушы'),
#         ('student', 'Оқушы'),
#     )
#     type = forms.ChoiceField(required=True, choices = CHOICES)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['username'].help_text = "Атыңыз"
#         self.fields['username'].label = 'Логин'
#         self.fields['username'].help_text = "Міндетті. Логин 150 таңба немесе одан аз болуы. Тек әріптер, цифрлар ғана болуы керек."
#         self.fields['password'].label = 'Құпия сөз'
#         self.fields['confirm_password'].label = 'Құпия сөзді қайталаңыз'
#         self.fields['first_name'].label = 'Фамилия'
#         self.fields['last_name'].label = 'Аты'
#         self.fields['email'].label = 'email'
#         self.fields['avatar'].label = 'Аватар'
#         self.fields['type'].label = 'Қолданушы түрін таңдаңыз'

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError('Бұл почта жүйеде тіркелген',code='invalid')
    #     return email
    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     if User.objects.filter(username=username).exists():
    #         raise forms.ValidationError('Бұл логин жүйеде тіркелген',code='invalid')
    #     return username
    # class Meta:
    #     model = User
    #     fields = ['username', 'password', 'confirm_password', 'first_name', 'last_name', 'email', 'avatar', 'type']
        

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'user'
        self.fields['username'].help_text = ''
        self.fields['password'].label = 'password'
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(username + " - not found")
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError("wrong password")
        return self.cleaned_data

# class CourseCreateForm(forms.ModelForm):
#     description = forms.CharField(widget=CKEditorWidget(),label="Сипаттамасы")
#     aim = forms.CharField(widget=CKEditorWidget(),label="Мақсаты")
#     class Meta:
#         model = Course
#         fields = ['category', 'title','aim', 'description','cover']

# class CourseContentCreateForm(forms.ModelForm):
#     text = forms.CharField(widget=CKEditorWidget(),label="Текст")
#     homework = forms.CharField(widget=CKEditorWidget(),label="Үй тапсырмасы")
#     class Meta:
#         model = CourseContent
#         fields = ['priority', 'title', 'video' ,'text','document', 'homework']

# class HomeWorkForm(forms.ModelForm):
#     class Meta:
#         model = HomeWork
#         fields = ['title', 'file']



