from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.list_posts, name='list_posts'),
    path('create/', views.create_post, name='create_post'),
    path('like_dislike/<int:post_id>/<str:action>/', views.like_dislike_post, name='like_dislike'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
]

