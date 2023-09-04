from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Categories'

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'

class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)
    # 삭제시, 포스트도 삭제 - author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # 삭제시, 작성자만 삭제
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    # 여기서 자체 생성한 클래스는 위에 올려두기
    tags = models.ManyToManyField(Tag, blank=True)

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d', blank=True)
    file_upload = models.FileField(upload_to="blog/files//%Y/%m/%d", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # author : 타 테이블의 주요키이자 이 테이블에서 외래키
    def __str__(self):
        return f'[{self.pk}]{self.title} :: {self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def PK_KEY(self):
        return f'{self.pk}'

    # 파일명
    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    # 파일의 확장자
    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]

