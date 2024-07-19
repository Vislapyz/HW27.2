from django.urls import path
from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig
from users.views import UserViewSet, PaymentLiatAPIView, PaymentCreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = UsersConfig.name
router = DefaultRouter()
router.register(r"user", UserViewSet, basename="user")
# router.register("payments", PaymentLiatAPIView)

urlpatterns = [
    path("payments/", PaymentLiatAPIView.as_view(),
                       name="payments"),
    path("payment/create/", PaymentCreateAPIView.as_view(),
                       name="payment_create"),

    path(
        "token/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
] + router.urls
