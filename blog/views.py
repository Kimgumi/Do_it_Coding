from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Category, Tag
from django.core.exceptions import PermissionDenied

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

class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = [
        'title', 'hook_text', 'content', 'file_upload', 'head_image'
    ]
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = [
        'title', 'hook_text', 'content', 'file_upload', 'head_image'
    ]
    template_name = 'blog/post_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

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