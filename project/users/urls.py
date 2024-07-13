from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import CustomTokenObtainPairView, CustomTokenLogoutView
from users.views import RegisterView, EmergencyContactCreateView, EmergencyContactListView
from django.urls import path

urlpatterns = [
    # Auth
    path("auth/login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/logout/", CustomTokenLogoutView.as_view(), name="token_logout"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    path('emergency-contact/<int:id>/register/', EmergencyContactCreateView.as_view(), name='emergecy-contact-register'),
    path('emergency-contact/', EmergencyContactListView.as_view(), name='emergecy-contact-list'),
]
