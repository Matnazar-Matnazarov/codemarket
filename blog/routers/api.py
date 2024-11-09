from rest_framework.routers import DefaultRouter
from django.urls import path, include
from ..api_views.view_blog_post import PostViewSet
from ..api_views.view_comment import CommentViewSet

blog_router = DefaultRouter()
comment_router = DefaultRouter()


# Separate routers for each logical group
blog_router = DefaultRouter()
comment_router = DefaultRouter()

# Blog API
blog_router.register(r"posts", PostViewSet, basename="post")

# Comments API
comment_router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("blog/", include(blog_router.urls)),  # Blog related endpoints
    path("comment/", include(comment_router.urls)),  # Comment related endpoints
]
