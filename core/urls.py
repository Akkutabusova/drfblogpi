from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #API TOKEN MANAGEMENT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #PROJECT URLS
    path('admin/', admin.site.urls),
    #USER MANAGEMENT
    path('api/user/', include('users.urls', namespace='users')),
    #BLOG_API APPLICATION
    path('api/', include('blog_api.urls', namespace='blog_api')),
    #API SCHEMA AND DOCUMENTATION
    path('docs/', include_docs_urls(title='BlogAPI')),
    path('schema', get_schema_view(
        title="Blog Api",
        description="API for blog api.",
        version="1.0.0"
    ), name='openapi-schema'),
    #OTHER
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include('blog.urls', namespace='blog')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)