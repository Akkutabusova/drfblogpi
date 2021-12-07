import json

from rest_framework import serializers
from blog.models import Post, Category, Comment, Bookmark, Favorites, PostArray
from django.conf import settings


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ('email', 'user_name', 'first_name')
        extra_kwargs = {'password': {'write_only': True}}


class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class PostArraySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostArray
        fields = ('id', 'index', 'image', 'text')


class PostSerializer(serializers.ModelSerializer):
    content = PostArraySerializer(many=True)

    class Meta:
        model = Post
        # fields = ('category', 'id', 'title', 'image', 'slug', 'date', 'author',
        #           'excerpt', 'status', 'blog_views')
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        data = validated_data.pop('content')
        instance = Post.objects.create(**validated_data)
        # content = json.load(data)
        for object in data:
            PostArray.objects.create(
                post=instance, **object)
        return instance


    # def create(self, validated_data):
    #     content_data = validated_data.pop('content')
    #     # validated_data['content'] = len(content_data)
    #     post = Post.objects.create(**validated_data)
    #     for cd in content_data:
    #         PostArray.objects.create(post=post, **cd)
    #     return post

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'body', 'author', 'post']


class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ('author', 'category')


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ('created', 'author', 'post')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'image')
