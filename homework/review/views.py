from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import render, redirect
from .forms import PostForm, CommentForm, UserForm, find_userForm, find_passworForm, reset_passwordForm, searchForm
from .models import Post, Comment, MyUser, Find
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from random import *
import random
import string
import requests
from bs4 import BeautifulSoup
# Create your views here.

def find_naver(request):
    if request.method == 'POST':
        word = request.POST['search']
        URL = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query='
        query = word

        fullURL = URL + query
        data = requests.get(fullURL).text
        soup = BeautifulSoup(data, 'html.parser')
        news_titles = soup.find_all(class_='_sp_each_title')
        title_list=[]
        for title in news_titles:
            title_list.append({'url' : title.get('href'), 'title' : title.get('title')})

        return render(request, 'find.html', {'title_list' : title_list})
    else:
        form = searchForm()
        return render(request, 'find.html', {'form' : form, 'message' : '정상적'})

def find_username(request):
    if request.method == 'POST':
        input_firstname = request.POST['first_name']
        input_lastname = request.POST['last_name']
        input_email = request.POST['email']

        for myuser in MyUser.objects.all():
            if input_firstname == myuser.first_name and input_lastname == myuser.last_name and input_email == myuser.email:
                username = myuser.username
                return render(request, 'registration/find_username.html', {'username': username})
        error = '아이디가 없습니다 ㅜ.ㅜ'
        return render(request, 'registration/find_username.html', {'error': error})
    else:
        form = find_userForm()
        return render(request, 'registration/find_username.html', {'form' : form})

def find_password(request):
    if request.method == 'POST':
        input_username = request.POST['username']
        input_firstname = request.POST['first_name']
        input_lastname = request.POST['last_name']
        input_email = request.POST['email']
        for myuser in MyUser.objects.all():
            if input_username == myuser.username and input_firstname == myuser.first_name and input_lastname == myuser.last_name and input_email == myuser.email:
                user = myuser
                letters = string.ascii_lowercase
                temp_pass=''
                for i in range(10):
                    temp_pass.join(random.choice(letters))
                user.set_password(temp_pass)
                user.save()
                message = '임시 비번입니다. 이걸로 로그인하세여'
                return render(request, 'registration/find_password.html', {'message' : message, 'temp_pass':temp_pass})
        error = '일치하는 비번이 없습니다 ㅜ.ㅜ'
        return render(request, 'registration/find_password.html', {'error': error})
    else:
        form = find_passworForm()
        return render(request, 'registration/find_password.html', {'form' : form})

def reset_password(request, myuser_pk):
    if request.method == 'POST':
        user = request.user
        form = reset_passwordForm(request.POST)
        if request.POST['password'] != request.POST['password_check']:
                error = "비밀번호가 일치하지 않습니다"
                return render(request, 'registration/reset_password.html', {'form': form, 'error': error})

        user.set_password(request.POST['password'])
        user.save()
        message = '비밀번호가 성공적으로 재설정 되었습니다'
        return render(request, 'registration/reset_password.html', {'message': message})
    else:
        form = reset_passwordForm()
        return render(request, 'registration/reset_password.html', {'form' : form})


        
def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        password1 = request.POST['password']
        password2 = request.POST['password_check']
        age = int(request.POST['age'])
        if password1 != password2 or age<15:
            if password1 != password2:
                error = "비밀번호가 일치하지 않습니다"
            else:
                error ="미성년자는 가입할 수 없습니다"
            return render(request, 'registration/signup.html', {'form': form, 'error': error})
        if form.is_valid():
            new_user = MyUser.objects.create_user(**form.cleaned_data)
            auth.login(request, new_user)
            return redirect('home')
        else:
            error = form.errors
            form = UserForm()
            return render(request, 'registration/signup.html', {'form': form, 'error': error})
    else:
        form = UserForm()
    return render(request, 'registration/signup.html', {'form': form})


def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html', {'posts': posts})

@login_required
def new(request):
    if request.method =='POST':
        form = PostForm(request.POST, request.FILES)
        post= form.save(commit=False)
        post.author = request.user.get_username()
        post.save()
        return redirect('detail', post.pk)
    else:
        form = PostForm()
    return render(request, 'new.html', {'form':form})

def detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        comment=form.save(commit=False)
        comment.post = post
        comment.save()
        return redirect('detail', post.pk)
    else:
        form = CommentForm()
        return render(request, 'detail.html', {'post':post, 'form': form})

@login_required
def edit(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        post = form.save()
        return redirect('detail', post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'edit.html', {'form':form})

@login_required
def delete(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    post.delete()
    return redirect('home')

@login_required
def delete_comment(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)

    comment.delete()
    return redirect('detail', post_pk)