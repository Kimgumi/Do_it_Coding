from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Category, Tag

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

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = [
        'title', 'hook_text', 'content', 'file_upload', 'head_image'
    ]

def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'tag': tag,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
        }
    )
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