from rest_framework import generics, viewsets, filters, status
from rest_framework.views import APIView
from blog.models import Post, Category, Comment, Favorites, Bookmark
from .serializers import PostSerializer, PostCategorySerializer, CommentSerializer, FavoritesSerializer, \
    BookmarkSerializer, CategorySerializer
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, \
    BasePermission, IsAdminUser
from django.shortcuts import get_object_or_404
from datetime import datetime, date, time
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser


class PostUserWritePermission(BasePermission):
    message = 'Editing posts is restricted to the author only.'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user


# User Filter
# class PostList(generics.ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = PostSerializer

#     def get_queryset(self):
#         user = self.request.user
#         return Post.objects.filter(author=user)

class PostList(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Post.postobjects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.filter()

    def get_object(self):
        obj = super().get_object()
        obj.blog_views += 1
        obj.save()
        return obj


class PostListDetailfilter(generics.ListAPIView):
    queryset = Post.postobjects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^slug', '=category']

    # '^' Starts-with search.
    # '=' Exact matches.
    # '@' Full-text search. (Currently only supported Django's PostgreSQL backend.)
    # '$' Regex search.


class PostListCategoryfilter(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        category = self.kwargs['category']
        return Post.objects.filter(category=category)

    # '^' Starts-with search.
    # '=' Exact matches.
    # '@' Full-text search. (Currently only supported Django's PostgreSQL backend.)
    # '$' Regex search.


class PostCategoryDetail(generics.RetrieveAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter()


class CategoryFavoritesfilter(generics.ListAPIView):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=author']


class Bookmarkfilter(generics.ListAPIView):
    serializer_class = BookmarkSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Bookmark.objects.filter(author=user)


class PostSearch(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^title']


# class CreatePost(generics.CreateAPIView):
#     permission_classes = [IsAdminUser]
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

class CreatePost(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    # parser_classes = [MultiPartParser, FormParser]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # def post(self, request, format=None):
    #     print(request.data)
    #     serializer = PostSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminPostDetail(generics.RetrieveAPIView):
    permission_classes = [IsAdminUser]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class EditPost(generics.UpdateAPIView):
    permission_classes = [PostUserWritePermission]
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class DeletePost(generics.RetrieveDestroyAPIView):
    permission_classes = [PostUserWritePermission]
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostCategoriesList(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostCategorySerializer
    queryset = Category.objects.all()


class CommentList(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentDetail(generics.RetrieveAPIView):
    queryset = Comment.objects.filter()
    serializer_class = CommentSerializer


class CreateComment(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(Post, slug=item)


class DeleteComment(generics.RetrieveDestroyAPIView):
    permission_classes = [PostUserWritePermission, IsAdminUser]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(Post, slug=item)


class CreateBookmark(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    # parser_classes = [MultiPartParser, FormParser]
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer


class DeleteBookmark(generics.RetrieveDestroyAPIView):
    permission_classes = [PostUserWritePermission, IsAdminUser]
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer


class CreateFavorite(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    # parser_classes = [MultiPartParser, FormParser]
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer


class DeleteFavorite(generics.RetrieveDestroyAPIView):
    permission_classes = [PostUserWritePermission, IsAdminUser]
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer

    # Define Custom Queryset
    # def get_queryset(self):
    #     return Post.objects.all()


# class PostList(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = Post.postobjects.all()

#     def list(self, request):
#         serializer_class = PostSerializer(self.queryset, many=True)
#         return Response(serializer_class.data)

#     def retrieve(self, request, pk=None):
#         post = get_object_or_404(self.queryset, pk=pk)
#         serializer_class = PostSerializer(post)
#         return Response(serializer_class.data)

# def list(self, request):
#     pass

# def create(self, request):
#     pass

# def retrieve(self, request, pk=None):
#     pass

# def update(self, request, pk=None):
#     pass

# def partial_update(self, request, pk=None):
#     pass

# def destroy(self, request, pk=None):
#     pass

# class PostList(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = Post.postobjects.all()
#     serializer_class = PostSerializer


""" Concrete View Classes
# CreateAPIView
Used for create-only endpoints.
# ListAPIView
Used for read-only endpoints to represent a collection of model instances.
# RetrieveAPIView
Used for read-only endpoints to represent a single model instance.
# DestroyAPIView
Used for delete-only endpoints for a single model instance.
# UpdateAPIView
Used for update-only endpoints for a single model instance.
# ListCreateAPIView
Used for read-write endpoints to represent a collection of model instances.
RetrieveUpdateAPIView
Used for read or update endpoints to represent a single model instance.
# RetrieveDestroyAPIView
Used for read or delete endpoints to represent a single model instance.
# RetrieveUpdateDestroyAPIView
Used for read-write-delete endpoints to represent a single model instance.
"""