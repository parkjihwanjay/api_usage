from django import forms
from .models import Post, Comment

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
   