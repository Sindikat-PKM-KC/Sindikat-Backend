from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import RegisterView, EmergencyContactCreateView
from django.urls import path

urlpatterns = [
    # Auth
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    #
    # Users
    path(
        "users/emergency-contact/",
        EmergencyContactCreateView.as_view(),
        name="emergency-contact",
    ),
]
