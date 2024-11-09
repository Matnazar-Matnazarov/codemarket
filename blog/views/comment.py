from django.views import View
from ..models.model_comment_on_blog_post import Comment
from ..forms import CommentForm
from django.shortcuts import render, redirect
from ..models.model_blog_post import Post


class CommentView(View):
    def get(self, request, post_id):
        post = Post.objects.select_related("user").filter(id=post_id).first()
        comments = Comment.objects.select_related("user", "post").filter(post=post)
        form = CommentForm(initial={"post": post, "user": request.user})
        context = {"post": post, "comments": comments, "form": form}
        return render(request, "blog/comment.html", context)

    def post(self, request, post_id):
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.comment = request.POST.get("comment")
                comment.post_id = post_id
                comment.user = request.user

                comment.save()
                return redirect("blog:blog_post", post_id=post_id)

        post = Post.objects.select_related("user").filter(id=post_id).first()
        comments = Comment.objects.select_related("user", "post").filter(post=post)
        context = {"post": post, "comments": comments, "form": form}
        return render(request, "blog/comment.html", context)
