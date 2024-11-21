from django.urls import path
from .routers.api import urlpatterns as api_urls
from .views.blog import BlogView, BlogPostView, BlogCommentView

# app_name = "api-blog"

urlpatterns = api_urls
urlpatterns += [
    path("", BlogView.as_view(), name="blog"),
    path("<str:title>/", BlogPostView.as_view(), name="blog_post"),
    path("comments/<str:title>/", BlogCommentView.as_view(), name="comments"),
]
