from django.db import models
from blog.models import Post

# Create your models here.
def landing(request):
    recent_posts = Post.objects.order_by('-pk')[:3]
    return render(
        request,
        'sing_pages/landing.html',
        {
            'recent_posts': recent_posts
        }
    )