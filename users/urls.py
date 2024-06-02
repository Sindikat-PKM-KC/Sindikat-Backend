from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, EmergencyContactCreateView
from django.urls import path

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "emergency-contact/",
        EmergencyContactCreateView.as_view(),
        name="emergency-contact-create",
    ),
]
