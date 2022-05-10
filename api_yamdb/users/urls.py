from django.urls import path, include
from rest_framework.routers import SimpleRouter


from users.views import SignUpViewSet, UserCreateViewSet, AuthViewSet

router = SimpleRouter()

router.register('v1/auth/signup', SignUpViewSet)
router.register('v1/auth/token', AuthViewSet)
router.register('v1/users', UserCreateViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
