from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # author : 타 테이블의 주요키이자 이 테이블에서 외래키
    def __str__(self):
        return f'[{self.pk}]{self.title}'