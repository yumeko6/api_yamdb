from django.urls import include, path
from rest_framework import routers

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet
from api.views import ReviewViewSet, CommentViewSet

app_name = 'api'

router = routers.DefaultRouter()

router.register(
    'genres',
    GenreViewSet,
    basename='genres')
router.register(
    'categories',
    CategoryViewSet,
    basename='categories')
router.register(
    'titles',
    TitleViewSet,
    basename='titles')

router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
]
