# projects/utils/check_post_tags.py
from django.shortcuts import render, redirect
from blog.models.model_blog_post import Post, Tags


def check_post_tags(request):
    post = Post.objects.first()
    if not post:
        return
    tag = Tags.objects.create(name="Python", slug="python", content_object=post)
    # post.tags.add(tag)
    # post.save()
    return render(request, "blog/post_detail.html", {"post": post})
