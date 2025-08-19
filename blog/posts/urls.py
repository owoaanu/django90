from django.urls import path
from .views import PostDetailView, PostListView

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail')
    # path('post/<int:post_id>/', views.post_detail, name='post_detail')
]