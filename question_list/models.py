from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User as jUser
from django import urls
from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import UserManager

# Create your models here.
    
class UserManager(models.Manager):
    def create_user(self, user):
        ouser = self.create(user=user)
        ouser.user.id = user.id 
        return ouser



class User(models.Model):
    def __str__(self):
        return self.user.username
    user = models.OneToOneField(jUser, related_name='profile', on_delete=models.CASCADE)
    avatar = models.FileField(upload_to='users_avatars', blank=True)
    rating = models.IntegerField(default=0)
    objects = UserManager()

    def edit_username(username, this_user):
        user = User.user_exists(username=username)
        if user is not None:
            return False
        else:
            juser = jUser.objects.get(username=this_user)
            juser.username = username
            juser.save()
            return True

    def edit_email(email, this_user):
        tuser = jUser.objects.filter(email=email)
        if tuser is not None:
            return False
        else:
            juser = jUser.objects.get(username=this_user)
            juser.email = email
            juser.save()
            return True

    def edit_password(password, this_user):
        this_user.password = password
        this_user.save()

    # @receiver(post_save, sender=jUser)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         User.objects.create(user=instance)

    # @receiver(post_save, sender=jUser)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()
    
    def user_exists(username):
        user = jUser.objects.filter(username=username)
        if user:
            return user
        else:
            return None

class Question(models.Model):
    def __str__(self):
        return self.title
    title = models.CharField(max_length=200)
    text = models.TextField()
    author = models.ForeignKey('User', related_name='questions', on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField('Tag', related_name='questions')
    rating = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created']

    def get_absolute_url(self):
        return "/question/%i" % self.id

class Answer(models.Model):
    def __str__(self):
        return self.text
    text = models.TextField(max_length=3000)
    author = models.ForeignKey('User', related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', related_name='answers', on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    rating = models.IntegerField(default=0)

    class Meta:
        ordering = ['-rating']

class Tag(models.Model):
    def __str__(self):
        return self.text
    text = models.CharField(max_length=20, unique=True)

    def get_absolute_tag_url(self):
        return "/tag/%s" % self.text

class Like(models.Model):
    author = models.ForeignKey('User', related_name='likes', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', related_name='likes', on_delete=models.CASCADE)
    answer = models.ForeignKey('Answer', related_name='likes', on_delete=models.CASCADE)
    is_like = models.BooleanField(default=False)

    # def like(self)


class AnswerModelForm(forms.ModelForm):
    class Meta: 
        model = Answer
        fields = ('text',)
        widgets = { 
            'text': forms.Textarea(attrs = {
                'rows': 5, 'cols': 120, 'class': "form-control", 'id': "questionBody", 'placeholder': "Type here..."
                }),
        }
         
        label='' 
        labels = { 'text': ('') }
        error_messages = {
            'text': {
                'max_length': ("This answer is too long."),
                'required': ("Please, enter an answer!"),
            },
        }

class JRegisterForm(forms.ModelForm):
    # def clean(self):
    #     cleaned_data = super(JRegisterForm, self).clean()
    #     username = cleaned_data.get("username")
    #     if not username:
    #         raise ValidationError("Please enter the username!")
    #     if jUser.objects.filter(username=username).exists():
    #         raise ValidationError("User exists!")
    #     password = cleaned_data.get("password")
    #     email = cleaned_data.get("email")
    #     if password and email:
    #         return cleaned_data
    #     else:
    #         raise ValidationError("Please fill all the fields!")

    class Meta: 
        model = jUser
        fields = ('username', 'password', 'email')
        widgets = { 
            'username': forms.TextInput(attrs = {
                'type':"login", 'class':"form-control col-md-10", 'id':"userLogin", 'aria-describedby':"loginHelp", 'placeholder':"Enter username"
                }),
            'password': forms.PasswordInput(attrs = {
                'type':"password", 'class':"form-control col-md-10", 'id':"userEmail", 'aria-describedby':"passwordlHelp", 'placeholder':"Enter password"
                }),
            'email': forms.TextInput(attrs = {
                'type':"email", 'class':"form-control col-md-10", 'id':"userMail", 'aria-describedby':"emailHelp", 'placeholder':"Enter email"
                }),
        }
        labels = {
            'username': ('Username'),
            'password': ('Password'),
            'email': ('Email'),
        }
        error_messages = {
            'username': {
                'max_length': ("This answer is too long."),
                'required': ("Please, enter an answer!"),
            },
        }

class CustomRegForm(forms.ModelForm):
    class Meta: 
        model = User
        fields = ('avatar', 'user')
        widgets = { 
            'avatar': forms.FileInput(attrs = {
                'type':"file", 'class':"custom-file-input is-valid", 'id':"validatedCustomFile"
                })
        }
        labels = { 
            'avatar': (''),
        }

class AskForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(AskForm, self).clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")
        if title and text:
            return cleaned_data
        else:
            raise ValidationError("Please fill all the fields!")

    def append_tags(self, question):
        taglist = self.cleaned_data['tags'].split(',', maxsplit=5)
        print(taglist)
        for tag in taglist:
            if not Tag.objects.filter(name=tag).exists():
                question.tags.create(name=tag)
            else:
                question.tags.add(Tag.objects.get(name=tag))

    # def save(self, commit=True):
    #     stag = super(AskForm, self).save(commit=commit)
    #     tags_list = self.cleaned_data.get('tags', None)
    #     if tags_list is not None:
    #         for tag in tags_list.split(","):
    #            if not Tag.objects.filter(name=tag).exists():
    #             question.tags.create(name=tag)
    #         else:
    #             question.tags.add(Tag.objects.get(name=tag))
    #     stag.save()
    #     return stag
                
    class Meta:
        model = Question
        fields = ('title', 'text', 'tags',)
        widgets = { 
            'title': forms.TextInput(attrs = {
                'type':"text", 'class':"form-control col-md-10", 'id':"userLogin", 'placeholder':"Enter title"
                }),
            'text': forms.Textarea(attrs = {
                'rows': 10, 'cols': 80, 'class': "form-control col-md-10", 'id': "questionBody", 'placeholder': "Type here..."
                }),
            # 'tags': forms.TextInput(attrs = {
            #     'type':"text", 'class':"form-control col-md-10", 'id':"userMail", 'aria-describedby':"emailHelp", 'placeholder':"Enter tags divided by comma"
            #     }),
        }
        labels = { 
            'title': ('Title'),
            'text': ('Question'),
            'tags': ('Tags'),
        }
        error_messages = {
            'title': {
                'required': ("Please, enter a title!"),
            },
            'text': {
                'required': ("Please, enter a question!"),
            },
            'tags': {
                'required': ("Please, enter tags!"),
            },
        }
