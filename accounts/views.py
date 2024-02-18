from django.shortcuts import render
from django.http import JsonResponse
from .models import Blog, Comments, Response
from django.core.serializers import serialize
from django.db.models import Count, Sum
from datetime import datetime, timedelta
from django.db.models import Count
from django.utils import timezone
from django.db.models import Max
from django.core.exceptions import ObjectDoesNotExist


def specific_author_blogs(request):
    if request.GET.get("userId"):
        userId = request.GET.get("userId")

        author_blogs = Blog.objects.filter(author_id=userId)
        blogs_data = []

        for blog in author_blogs:
            likes_count = Response.objects.filter(blog=blog, like_or_not=True).count()
            dislikes_count = Response.objects.filter(
                blog=blog, like_or_not=False
            ).count()
            comments_count = Comments.objects.filter(blog=blog).count()

            # Serialize the User object to include its attributes in the response
            author_serialized = serialize(
                "json", [blog.author], fields=("id", "username")
            )

            blog_data = {
                "id": blog.id,
                "name": blog.name,
                "content": blog.content,
                "author": author_serialized,
                "created_date": blog.created_date,
                "likes_count": likes_count,
                "dislikes_count": dislikes_count,
                "comments_count": comments_count,
            }
            blogs_data.append(blog_data)

        response_data = {"blogs_data": blogs_data}
        return JsonResponse(response_data, safe=False)


def home(request):
    blogs = Blog.objects.all
    context = {"blogs_data": blogs}
    return render(request, "specific_author_blogs.html", context)


def get_top_commented_blogs(request):
    if request.GET.get("userId"):
        userId = request.GET.get("userId")
        print(userId, "896325")

        blogs = Blog.objects.filter(author_id=userId)
        top_commented_blogs = (
            Comments.objects.filter(blog__in=blogs)
            .values("blog__id", "blog__name")
            .annotate(comment_count=Count("id"))
            .order_by("-comment_count")[:5]
        )

        top_commented_blogs_list = list(top_commented_blogs)

        data = {"top_commented_blogs": top_commented_blogs_list}
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({"error": "UserId not provided in the request"}, status=400)


def like_and_dislike(request):
    now = timezone.now()
    three_days_ago = now - timedelta(days=3)

    top_liked_blogs = (
        Blog.objects.filter(
            response__like_or_not=True, response__response_date__gte=three_days_ago
        )
        .annotate(like_count=Count("response"))
        .order_by("-like_count")[:5]
    )

    top_disliked_blogs = (
        Blog.objects.filter(
            response__like_or_not=False, response__response_date__gte=three_days_ago
        )
        .annotate(dislike_count=Count("response"))
        .order_by("-dislike_count")[:5]
    )

    top_liked_blogs_list = list(top_liked_blogs.values())
    top_disliked_blogs_list = list(top_disliked_blogs.values())

    context = {
        "top_liked_blogs": top_liked_blogs_list,
        "top_disliked_blogs": top_disliked_blogs_list,
    }

    return JsonResponse(context, safe=False)


def get_recent_liked_blogs(request):
    userId = request.GET.get("userId")

    if not userId:
        return JsonResponse({"error": "UserId not provided in the request"}, status=400)

    recent_liked_blogs = (
        Blog.objects.filter(response__user_id=userId, response__like_or_not=True)
        .annotate(
            like_count=Count("response"),
            latest_response_date=Max("response__response_date"),
        )
        .order_by("-latest_response_date")[:5]
    )

    recent_liked = list(recent_liked_blogs.values())
    context = {
        "recent_liked_blogs": recent_liked,
    }
    print(recent_liked, "5682346964")

    return JsonResponse(context, safe=False)


def get_comment_history(
    request,
):
    try:
        blog_id = request.GET.get("blogId")
        blog = Blog.objects.get(id=blog_id)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Blog not found"}, status=404)

    comment_history = (
        Comments.objects.filter(blog=blog)
        .values("user__username", "comment_text", "created_date")
        .order_by("-created_date")
    )

    comment_history_list = list(comment_history)

    return JsonResponse({"comment_history": comment_history_list}, safe=False)


def comment_history_view_author(request):
    author_id = request.GET.get("userId")
    print(author_id, "5656565")
    comment_history = Comments.objects.filter(user=author_id).select_related("blog")
    print(comment_history, "656565656")
    comment_history_list_author = list(comment_history.values())

    print(comment_history_list_author, "565646")
    return JsonResponse({"comment_history": comment_history_list_author}, safe=False)
