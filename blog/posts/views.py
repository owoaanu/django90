import datetime

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from .models import Post

from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.views import APIView #for api view
from rest_framework.permissions import IsAuthenticatedOrReadOnly #for api view

from rest_framework import generics, viewsets # for useing the generic view and viewset

from rest_framework import status, filters
from .serializers import PostListSerializer, PostDetailSerializer, PostSerializer
from .pagination import SmallResultsSetPagination

# Create your views here.

# django template view
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


# custom json reponse views
def api_greeting(request):
    return JsonResponse({"message":"Hello, API world!"})

def api_posts(request):
    posts = Post.objects.values("id", "title", "content", "created_at").all().order_by('-created_at')
    posts = posts[:5]
    # posts = Post.objects.all().values("id", "title", "content", "created_at")
    return JsonResponse(list(posts), safe=False)

# Function Based api view
@api_view(['GET'])
def post_list(request):
    posts = Post.objects.all()
    serializer = PostListSerializer(posts, many=True)
    return Response(serializer.data)


# APIView
class PostListAPIView(APIView):
    def get(selfself, request):
        posts = Post.objects.all()
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)

    def post(selfself, request):
        serializer = PostDetailAPIView(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return None

    def get(self, request, pk):
        post= self.get_object(pk)
        if not post:
            return Response({'error' : 'post not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post= self.get_object(pk)
        if not post:
            return Response({'error' : 'post not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostDetailSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post= self.get_object(pk)
        if not post:
            return Response({'error' : 'post not found'}, status=status.HTTP_404_NOT_FOUND)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Generic Views -- see simplicity
class PostListCreateAPIView(generics.ListCreateAPIView):
    # queryset = Post.objects.all()

    # challenge to include search
    def get_queryset(self):
        queryset = Post.objects.all()
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset
    serializer_class = PostSerializer


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# Viewsets
class PostViewset(viewsets.ModelViewSet):
    """
    API endpoint for managing blog posts.

    Endpoints:
    - List all posts (GET /api/posts/)
    - Retrieve single post (GET /api/posts/{id}/)
    - Create a new post (POST /api/posts/)
    - Update post (PUT/PATCH /api/posts/{id}/)
    - Delete post (DELETE /api/posts/{id}/)

    Notes:
    - Title is required (3–120 chars)
    - Body is required (text)
    """
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "content"]      # shows a search bar
    ordering_fields = ["created_at", "title"]  # shows an ordering dropdown
    # pagination_class = SmallResultsSetPagination

    meta_title = "Posts"
    meta_description = "Create and manage blog posts. Title + content are editable; created_at is read-only"

#     adding a custom action endpoint
    @action(detail=False, methods=['get'])
    def recent(self, request):
        recent_posts = Post.objects.order_by('-created_at')[:5]
        serializer = PostSerializer(recent_posts, many=True)
        return Response(serializer.data)

    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



