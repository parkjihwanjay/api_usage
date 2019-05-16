from django import forms
from .models import Post, Comment, MyUser
from django.contrib.auth.models import User

class reset_passwordForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['password', 'password_check']

        labels = {  
            'password' : '새 비밀번호',
            'password_check' : '새 비밀번호 확인',
        }

        widgets={
            'password' : forms.PasswordInput(attrs={'class':'password_form', 'rows' : '1'}),
            'password_check' : forms.PasswordInput(),
        }

class find_userForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name' : '이름',
            'last_name' : '성',
            'email' : '이메일 주소',
        }

        widgets={
            'first_name' : forms.Textarea(attrs={'class':'username_form', 'rows' : '1'}),
            'last_name' : forms.Textarea(attrs={'class':'username_form', 'rows' : '1'}),
            'email' : forms.Textarea(attrs={'class':'email_form', 'rows' : '1'}),
        }
class find_passworForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'email', 'username']
        labels = {
            'first_name' : '이름',
            'last_name' : '성',
            'email' : '이메일 주소',
            'username' : '아이디',
        }

        widgets={
            'first_name' : forms.Textarea(attrs={'class':'username_form', 'rows' : '1'}),
            'last_name' : forms.Textarea(attrs={'class':'username_form', 'rows' : '1'}),
            'email' : forms.Textarea(attrs={'class':'email_form', 'rows' : '1'}),
            'username' : forms.Textarea(attrs={'class':'username_form', 'rows' : '1'}),
        }

class UserForm(forms.ModelForm):

    class Meta:
        model = MyUser
        fields = ["username", 'first_name', 'last_name', 'email', 'password', 'password_check', 'age']
        labels = {
            'username' : '아이디',
            'first_name' : '이름',
            'last_name' : '성',
            'password' : '비밀번호',
            'email' : '이메일 주소',
            'password_check' : '비밀번호 확인',
            'age' : '나이',
        }

        widgets={
            'username' : forms.Textarea(attrs={'class':'username_form', 'rows' : '1'}),
            'first_name' : forms.Textarea(attrs={'class':'username_form', 'rows' : '1'}),
            'last_name' : forms.Textarea(attrs={'class':'username_form', 'rows' : '1'}),
            'password' : forms.PasswordInput(attrs={'class':'password_form', 'rows' : '1'}),
            'email' : forms.Textarea(attrs={'class':'email_form', 'rows' : '1'}),
            'password_check' : forms.PasswordInput(),
        }

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('username', 'password')
#         labels ={
#             'username':'아이디',
#             'password' : '비밀번호',
#         }
#         widgets={
#             'password' : forms.PasswordInput()
#         }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'contents', 'img', 'price', 'score')
        labels={
            'title': '제목',
            'contents' : '내용',
            'img' : '이미지 업로드',
            'price' : '가격',
            'score' : '점수'
        }
        widgets={
            'title' : forms.Textarea(attrs={'class':'title_form', 'rows' : '1'}),
            'contents' : forms.Textarea(attrs={'class':'contents_form', 'rows':'10'}),
            'price' : forms.NumberInput(attrs={'cols':'2', 'class':'price_form'}),
            'score' : forms.Select(attrs={'class':'score_form'})
        }
   
      

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields=('댓글',)

        widgets={
            '댓글': forms.Textarea(attrs={'class': 'comment_form', 'rows':'1'})
        }
   