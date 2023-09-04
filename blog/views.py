from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

# Create your views here.
#CBV로 여러 포스트 나열 목록 웹페이지 만들기
class PostList(ListView): #index함수 대체
    model = Post
    #ListView 클래스를 사용해 'model명_list.html'을 기본 템플릿으로 사용
    template_name = 'blog/post_list.html'
    ordering = '-pk' # 최신순

class PostDetail(DetailView): #single_post_page함수 대체
    model = Post
    template_name = 'blog/post_detail.html'

#FBV로 페이지 제작시 방법
# def index(request):
#     #posts = Post.objects.all()
#     posts = Post.objects.all().order_by('-pk')   #최신글부터
#     return render(
#         request,
#         'blog/index.html',
#         {
#             'posts': posts,
#         }
#     )
# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)
#
#     return render(
#         request,
#         'blog/single_post_page.html',
#         {
#             'post': post,
#         }
#     )