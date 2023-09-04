from django.urls import path
from . import views

urlpatterns = [
    path('tag/<str:slug>/', views.tag_page),
    path('create_post/', views.PostCreate.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('', views.PostList.as_view()), #CBV로 제공된 클래스인 ListView 사용
    #FBV - path('', views.index),
    #FBV - path('<int:pk>/', views.single_post_page),
]