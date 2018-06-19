from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User as jUser
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from .models import  *
from .forms import *

def listing(request):
    by_rating = request.GET.get('by_rating')
    if by_rating:
        queryset = Question.objects.get_hot()
    else:
        queryset = Question.objects.get_new()
    page = request.GET.get('page')
    questions = Paginator(queryset, 3).get_page(page)
    return render(request, 'question_list/index.html', {'questions': questions, 'page': page, 'by_rating': by_rating})

def question_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = question.answers.all()
    tags = question.tags.all()
    if request.method == 'POST':
        correct = request.GET.get('correct')
        if correct:
            answer = question.answers.get(id=correct)
            answer.is_correct = True;
            answer.save()
            form = AnswerModelForm()
            return render(request, 'question_list/question.html', {'question': question, 'answers': answers, 'tags': tags, 'form': form})
        form = AnswerModelForm(request.POST)
        if form.is_valid():
            new_answer = form.save(commit=False) 
            new_answer.question = question
            new_answer.author = User.objects.get(user=request.user)
            new_answer = form.save() 
            url = '{}#' + 'answer' + str(new_answer.id)
            return HttpResponseRedirect(url.format(reverse('question_list:question', args=(question.id,))))
        else:
            return render(request, 'question_list/question.html', {'question': question, 'answers': answers, 'tags': tags, 'form': form})
        
    form = AnswerModelForm()
    return render(request, 'question_list/question.html', {'question': question, 'answers': answers, 'tags': tags, 'form': form})

def tag(request, tag):
    questions = Question.objects.get_by_tag(tag)
    paginator = Paginator(questions, 3)
    page = request.GET.get('page')
    questions = paginator.get_page(page)
    return render(request, 'question_list/tag.html', {'questions': questions, 'tag': tag, 'page': page})

def ask(request):
    if not request.user.is_authenticated:
        url = "%s?dest_page=ask" % reverse('question_list:login')
        return HttpResponseRedirect(url)
    
    form = AskForm()
    if request.method == 'POST':
        form = AskForm(request.POST)
        # form.clean()
        if form.is_valid():
            question = form.save(commit=False)
            question.author = User.objects.get(user=request.user)
            # form.append_tags(question=question) 
            # clean_form = form.clean()
            question = form.save()
            return HttpResponseRedirect(reverse('question_list:question', args=(question.id,)))            
        else:
            return render(request, 'question_list/ask.html', { 'form': form })

    return render(request, 'question_list/ask.html', { 'form': form })

def log_in(request):
    form = LoginForm()
    dest_page = "question_list:%s" % request.GET.get('dest_page')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        form.is_valid()
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.GET.get('dest_page'):
                return HttpResponseRedirect(reverse(dest_page))
            return HttpResponseRedirect(reverse('question_list:index'))
        else:
            return render(request, 'question_list/login.html', {'credentials_mismatch': True, 'form': form})
    return render(request, 'question_list/login.html', {'form': form, 'login_error': request.GET.get('dest_page') })

def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('question_list:index'))

def register(request):
    jForm = JRegisterForm()
    if request.method == 'POST':
        jForm = JRegisterForm(request.POST)
        jForm.is_valid()
        if jForm.is_valid():
            jForm.save(commit=False)
            juser = jUser.objects.create_user(jForm.cleaned_data['username'], jForm.cleaned_data['email'], jForm.cleaned_data['password'])
            new_user = User.objects.create_user(juser)
            kuser = authenticate(request, username=jForm.cleaned_data['username'], password=jForm.cleaned_data['password'])
            if kuser is not None: 
                login(request, kuser)
                return HttpResponseRedirect(reverse('question_list:index'))
            return HttpResponseRedirect(reverse('question_list:register',  args={'jForm': jForm  }))
        else:
            return render(request, 'question_list/register.html', {'jForm': jForm})

    return render(request, 'question_list/register.html', {'jForm': jForm, })

def settings(request):
    form = EditForm()
    if request.method == 'POST':
        form = EditForm(request.POST)
        result = {}
        username = request.POST['username']
        if username:
            if User.edit_username(username=username, this_user=request.user.username):
                result['success'] = True
            else:
                result['user_exists'] = True
                return render(request, 'question_list/settings.html', {'form': form, 'result': result})

        email = request.POST['email']        
        if email:
            if User.edit_email(email=email, this_user=request.user.username):
                result['success'] = True
            else:
                result['email_exists'] = True
                return render(request, 'question_list/settings.html', {'form': form, 'result': result})
                
        password = request.POST['password']
        password2 = request.POST['password2']
        if not password==password2:
            result['passwords_do_not_match'] = True 
            return render(request, 'question_list/settings.html', {'form': form, 'result': result})
        else:
            User.edit_password(password=password, this_user=request.user)
            result['success'] = True
        return render(request, 'question_list/settings.html', {'form': form, 'result': result})

    return render(request, 'question_list/settings.html', {'form': form})