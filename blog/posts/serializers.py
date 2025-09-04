from rest_framework import serializers
from .models import Post

class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'created_at']

class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        help_text="Short, descriptive title (3–120 chars).",
        style={"placeholder": "My first post"},
        min_length=3,
        max_length=120,
    )
    content = serializers.CharField(
        style={"base_template": "textarea.html"},
        help_text="Full post content."
    )
    created_at = serializers.DateTimeField(read_only=True)



    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at']
