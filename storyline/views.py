"""Generate views for the project"""
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.views import generic, View
from django.contrib import messages
from .forms import CommentForm
from .models import Post


class PostList(generic.ListView):
    """List view for the posts."""
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6


class PostDetail(View):
    """Displays the detail of the post."""

    def get(self, request, slug, *args, **kwargs):
        """Get the post to read"""
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("created_on")
        liked = False
        if post.likes.filter(id=request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm(),
            },
        )

    def post(self, request, slug, *args, **kwargs):
        """Post a comment"""
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, "Your comment has been added.")
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "liked": liked,
                "comment_form": comment_form,
            },
        )


class PostLike(View):
    """View for liking a post."""

    def post(self, request, slug):
        """Toggle post"""
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        likes_count = post.likes.count()
        context = {"liked": liked, "likes_count": likes_count}
        if request.is_ajax():
            return JsonResponse(context)
        else:
            return JsonResponse(context, status=200)
        # return HttpResponseRedirect(reverse("post_detail", args=[slug]))
