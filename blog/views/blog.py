from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from ..models.model_blog_post import Post
from ..forms.comment import CommentForm
from ..models.model_comment_on_blog_post import Comment
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from hitcount.models import HitCount
from hitcount.views import (
    HitCountMixin,
)
from django.contrib import messages
from django.db.models import Count

class BlogView(View):
    def get(self, request):
        blog_posts = (
            Post.objects.select_related("author")
            .prefetch_related("tags", "comments_post_model")
            .annotate(comment_count=Count("comments_post_model"))
            .only(
                "title", "created_at", "body", "image", "icon_name",
                "author__email", "author__picture", "tags__name"
            )
            .all()
        )
        print(blog_posts)
        return render(request, "blog.html", {"blog_posts": blog_posts})


class BlogPostView(View):
    def get(self, request, title):
        blog_post = (
            Post.objects.select_related("author")
            .prefetch_related("tags")
            .only("title", "created_at", "author__email", "author__picture", "icon_name", "image", "body")
            .filter(title=title)
            .first()
        )
        if blog_post:
            context = {}
            comments = Comment.objects.select_related("user").filter(post=blog_post).order_by("-created_at")
            form = CommentForm() if request.user.is_authenticated else None
            context = {"blog_post": blog_post, "comments": comments, "form": form, "comment_count":comments.count()}

            # Cache the hit count
            hitcount = HitCount.objects.get_for_object(blog_post)
            hits = hitcount.hits
            context["hitcount"] = {"pk": hitcount.pk}

            # Use an instance of HitCountMixin to count the hits
            hitcount_mixin = HitCountMixin()
            hitcount_response = hitcount_mixin.hit_count(request, hitcount)
            if hitcount_response.hit_counted:
                hits += 1  # Increment hits only if it was counted
                context["hitcount"].update(
                    {"hit_counted": hitcount_response.hit_counted, "total_hits": hits}
                )

            return render(request, "post_detail.html", context)
        else:
            messages.error(request, "Blog post not found")
            return redirect("blog")


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
                    "picture": comment.user.picture.url if comment.user.picture else None,
                    "message": "Comment added successfully",
                },
                status=201,
            )

        return JsonResponse({"errors": form.errors}, status=400)
