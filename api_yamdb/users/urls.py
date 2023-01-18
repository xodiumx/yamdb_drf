from django.urls import include, path

from .views import (
    UserViewSet,
    SignUpViewSet,
    ReceiveJWTViewSet,
)
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')

signup = SignUpViewSet.as_view({'post': 'create'})
get_tokens = ReceiveJWTViewSet.as_view()

urlpatterns = [
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', get_tokens, name='token'),
    path('v1/', include(router_v1.urls)),
]
