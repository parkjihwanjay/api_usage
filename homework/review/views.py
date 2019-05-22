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
import requests,xmltodict, json
from bs4 import BeautifulSoup
from django.core.mail import EmailMessage
from review.api.api_key import *

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

def lol_find(request):
    if request.method == 'POST':
        lol_id = str(request.POST['search'])
        api_key = api_find()
        URL = f'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + lol_id + '?api_key=' + api_key

        data = requests.get(URL).json()

        id = str(data['id'])
        level = int(data['summonerLevel'])
        name = data['name']

        profile = {'name': name, 'level' : level}

        league = f'https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/' + id + '?api_key=' + api_key
        league_info = requests.get(league).json()

        # champions = f'https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/' + id + '?api_key=RGAPI-d9d4320c-94e2-49e2-a834-6cddbff83f6e'
        # champions_info = requests.get(champions).json()

        mastery = f'https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/' + id +'?api_key=' + api_key
        mastery_info = requests.get(mastery).json()

        # for champions_information in champions_info:
        #     name = champions_information['']
        temp_level = 0
        temp_point = 0

        for mastery_information in mastery_info:
            
            if mastery_information['championLevel'] >= temp_level:
                temp_level = int(mastery_information['championLevel'])

            if mastery_information['championPoints'] >= temp_point:
                temp_point = int(mastery_information['championPoints'])
        # for mastery_information in mastery_info:
            
            
        
        return render(request, 'lol_find.html', {'profile' : profile, 'league_info' : league_info, 'id' : id, 'championLevel' : temp_level, 'championPoints' : temp_point})
    else:
        form = searchForm()
        return render(request, 'lol_find.html', {'form' : form, 'message' : '정상적'})

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
                    temp_pass = temp_pass + random.choice(letters)
                user.set_password(temp_pass)
                user.save()
                subject = 'Django를 통해 발송된 메일입니다'
                message = 'Goolge 발송'
                mail = EmailMessage(subject, message, to=[input_email])
                mail.send()
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
        for myuser in MyUser.objects.all():
            if myuser.pk == myuser_pk:
                password_origin = myuser.password
                break
        if request.POST['password_origin'] == password_origin :
            if request.POST['password'] != request.POST['password_check']:
                    error = "비밀번호가 일치하지 않습니다"
                    return render(request, 'registration/reset_password.html', {'form': form, 'error': error})

            user.set_password(request.POST['password'])
            user.save()
            message = '비밀번호가 성공적으로 재설정 되었습니다'
            return render(request, 'registration/reset_password.html', {'message': message})
        else:
            message = '기존 비밀번호가 일치하지 않습니다.'
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