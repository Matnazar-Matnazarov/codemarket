from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from ..models.model_blog_post import Post
from ..forms.comment import CommentForm
from ..models.model_comment_on_blog_post import Comment
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class BlogView(View):
    def get(self, request):
        blog_posts = (
            Post.objects.select_related("author").prefetch_related("tags").all()
        )
        print(blog_posts)
        return render(request, "blog.html", {"blog_posts": blog_posts})


class BlogPostView(View):
    def get(self, request, title):
        blog_post = (
            Post.objects.select_related("author")
            .prefetch_related("tags")
            .filter(title=title)
            .first()
        )
        comments = Comment.objects.select_related("user").filter(post=blog_post)
        print(comments)
        form = CommentForm() if request.user.is_authenticated else None
        context = {"blog_post": blog_post, "comments": comments, "form": form}
        return render(request, "post_detail.html", context)


@method_decorator(login_required, name="dispatch")
class BlogCommentView(View):
    def post(self, request, title):
        blog_post = Post.objects.select_related("author").filter(title=title).first()

        if not blog_post:
            return JsonResponse({"error": "Blog post not found"}, status=404)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment.objects.create(
                comment=form.cleaned_data["comment"], user=request.user, post=blog_post
            )
            return JsonResponse(
                {
                    "comment": comment.comment,
                    "username": comment.user.email,
                    "created_at": comment.created_at.isoformat(),
                },
                status=201,
            )

        return JsonResponse({"errors": form.errors}, status=400)
