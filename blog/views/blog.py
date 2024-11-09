from django.shortcuts import render, redirect
from django.views import View
from ..models.model_blog_post import Post
from ..forms import PostForm


class BlogView(View):
    def get(self, request):
        blog_posts = Post.objects.select_related("user").all()
        return render(request, "blog/blog.html", {"blog_posts": blog_posts})


class BlogPostView(View):
    def get(self, request, post_id):
        blog_post = Post.objects.select_related("user").filter(id=post_id).first()
        return render(request, "blog/blog_post.html", {"blog_post": blog_post})
