from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from blog.models import Post, Category, Comment, Bookmark, Favorites, PostArray
from django.conf import settings

class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Remove escape slashes
            escapes = ''.join([chr(char) for char in range(1, 32)])
            translator = str.maketrans('', '', escapes)
            data = data.translate(translator)
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

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
    image = Base64ImageField(
        max_length=None, use_url=True, allow_null=True
    )
    class Meta:
        model = PostArray
        fields = ('id', 'index', 'image', 'text')


class PostSerializer(serializers.ModelSerializer):
    content = PostArraySerializer(many=True)
    image = Base64ImageField(
        max_length=None, use_url=True, allow_null=True
    )

    class Meta:
        model = Post
        # fields = ('category', 'id', 'title', 'content', 'image', 'slug', 'date', 'author',
        #           'excerpt', 'status', 'blog_views')
        fields = '__all__'
        # depth = 1

    def create(self, validated_data):
        data = validated_data.pop('content')
        instance = Post.objects.create(**validated_data)
        # content = json.load(data)
        for obj in data:
            PostArray.objects.create(
                post=instance, **obj)
        return instance

    def __init__(self, *args, **kwargs):
        super(PostSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1

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
    image = Base64ImageField(
        max_length=None, use_url=True,
    )
    class Meta:
        model = Category
        fields = ('id', 'name', 'image')
