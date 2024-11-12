from django.shortcuts import render, redirect
from django.views import View
from ..models.model_blog_post import Post
from ..forms import PostForm


class BlogView(View):
    def get(self, request):
        blog_posts = Post.objects.select_related("user").prefetch_related("tags").all()
        print(blog_posts)
        return render(request, "blog.html", {"blog_posts": blog_posts})


class BlogPostView(View):
    def get(self, request, slug):
        blog_post = Post.objects.select_related("user").prefetch_related("tags").filter(slug=slug).first()
        return render(request, "post_detail.html", {"blog_post": blog_post})
