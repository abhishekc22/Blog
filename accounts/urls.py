from django.urls import path
from . import views

urlpatterns = [
    path(
        "specific_author_blogs",
        views.specific_author_blogs,
        name="specific_author_blogs",
    ),
    path("", views.home, name="home"),
    path(
        "get_top_commented_blogs/",
        views.get_top_commented_blogs,
        name="get_top_commented_blogs",
    ),
    path("like_and_dislike/", views.like_and_dislike, name="like_and_dislike"),
    path(
        "get_recent_liked_blogs/",
        views.get_recent_liked_blogs,
        name="get_recent_liked_blogs",
    ),
    path("get_comment_history/", views.get_comment_history, name="get_comment_history"),
    path(
        "comment_history_view_author/",
        views.comment_history_view_author,
        name="comment_history_view_author",
    ),
]
