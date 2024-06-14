from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import RegisterViewSet, EmergencyContactCreateViewSet
from django.urls import path
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r"auth/register", RegisterViewSet, basename="register")
router.register(
    r"users/emergency-contact",
    EmergencyContactCreateViewSet,
    basename="emergency-contact",
)

urlpatterns = [
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

urlpatterns += router.urls
