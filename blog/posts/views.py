from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Post

# Create your views here.
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    # posts = [Post.objects.get(id=1)]
    # posts = Post.objects.filter(title__icontains='django')
    # posts = Post.objects.all()
    return render(request, 'posts/home.html',{'posts':posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'posts/post_detail.html', {'post':post})


class PostListView(ListView):
    model = Post
    template_name = 'posts/home.html'
    context_object_name = 'posts'


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'
