from django.db import models

# Create your models here.
class Post(models.Model):
    img = models.FileField(null=True)
    title = models.CharField(max_length=200)
    contents = models.TextField()
    price = models.SmallIntegerField()
    
    choices_in_score=(
        ('1점', '1'),
        ('2점', '2'),
        ('3점', '3'),
        ('4점', '4'),
        ('5점', '5'),
        ('6점', '6'),
        ('7점', '7'),
        ('8점', '8'),
        ('9점', '9'),
        ('10점', '10'),
    )

    score = models.CharField(
        max_length=100,
        choices = choices_in_score,
        default='5점',
    )

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    댓글 = models.CharField(max_length=150)
