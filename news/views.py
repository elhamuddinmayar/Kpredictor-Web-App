from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Post, LikeDislike, Comment
from django.db.models import Count, Q

@login_required
def create_post(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        image = request.FILES.get('image')
        video = request.FILES.get('video')

        if not (text or image or video):
            error = "Please provide text, image, or video."
            return render(request, 'news/create_post.html', {'error': error})

        Post.objects.create(
            author=request.user,
            text=text,
            image=image,
            video=video,
        )
        return redirect('posts:list_posts')

    return render(request, 'news/create_post.html')


def list_posts(request):
    posts = Post.objects.annotate(
        likes_count=Count('votes', filter=Q(votes__vote=1)),
        dislikes_count=Count('votes', filter=Q(votes__vote=-1))
    ).order_by('-created_at')

    return render(request, 'news/list_posts.html', {'posts': posts})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            Comment.objects.create(user=request.user, post=post, text=text)
    return redirect('posts:list_posts')


@login_required
def like_dislike_post(request, post_id, action):
    post = get_object_or_404(Post, id=post_id)
    vote_value = 1 if action == 'like' else -1

    obj, created = LikeDislike.objects.update_or_create(
        user=request.user,
        post=post,
        defaults={'vote': vote_value}
    )
    data = {
        'likes': post.votes.filter(vote=1).count(),
        'dislikes': post.votes.filter(vote=-1).count(),
    }
    return JsonResponse(data)
