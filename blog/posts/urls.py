from django.urls import path, include
from .views import PostDetailAPIView, PostListAPIView, PostListCreateAPIView, PostRetrieveUpdateDestroyAPIView
from .views import  PostViewset
from rest_framework.routers import  DefaultRouter

router = DefaultRouter()
router.register(r'posts', PostViewset, basename='post')

urlpatterns = [
    # Class basedView urls
    # path('', PostListView.as_view(), name='home'),
    # path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),

    # APIView - Day 10
    # path('api/posts/', PostListAPIView.as_view(), name='post-list'),
    # path('api/posts/<int:pk>', PostDetailAPIView.as_view(), name='post-detail'),

    # Generic View urls - Day 11
    # path('api/posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    # path('api/posts/<int:pk>', PostRetrieveUpdateDestroyAPIView.as_view(), name='post-detail'),

    #ViewSets - Day 12
    path('api/', include(router.urls)),

    # path('post/<int:post_id>/', views.post_detail, name='post_detail')
]