from .views import  DeletePost, PostCategoriesList, PostListCategoryfilter, CategoryFavoritesfilter, Bookmarkfilter
from .views import PostList, PostDetail, PostListDetailfilter,CreatePost, AdminPostDetail, EditPost, CommentList, CommentDetail, CreateComment, DeleteComment
#from rest_framework.routers import DefaultRouter
from django.urls import path

app_name = 'blog_api'

# router = DefaultRouter()
# router.register('', PostList, basename='post')
# urlpatterns = router.urls

urlpatterns = [
    path('posts/', PostDetail.as_view(), name='detailcreate'),
    path('search/', PostListDetailfilter.as_view(), name='postsearch'),
    path('', PostList.as_view(), name='listcreate'),
    #Bookmark
    path('bookmarks/ ',Bookmarkfilter.as_view()),
    #Category
    path('categories/',PostCategoriesList.as_view(), name='listcategories'),
    path('category/', PostListCategoryfilter.as_view(), name='postsbycategory'),
    #Favorites
    path('favorites/',CategoryFavoritesfilter.as_view()),
    #Comments
    # code omitted for brevity
    path('comments/',CommentList.as_view()),
    path('comments/<int:pk>/', CommentDetail.as_view()),
    path('comments/create/',CreateComment.as_view()),
    path('comments/delete/',DeleteComment.as_view()),
    #Post Admin Urls
    path('admin/create/',CreatePost.as_view(), name='createpost'),
    path('admin/edit/postdetail/<int:pk>', AdminPostDetail.as_view(), name='admindetailpost'),
    path('admin/edit/<int:pk>/', EditPost.as_view(), name='editpost'),
    path('admin/delete/<int:pk>/', DeletePost().as_view(), name='deletepost'),
]