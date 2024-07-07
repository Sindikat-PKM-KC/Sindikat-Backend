from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenObtainPairView
from users.views import RegisterView, EmergencyContactCreateView, EmergencyContactListView
from django.urls import path

urlpatterns = [
    # Auth
    path("auth/login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/register/", RegisterView.as_view(), name="register"),

    path('emergency-contact/<int:id>/register/', EmergencyContactCreateView.as_view(), name='emergecy-contact-register'),
    path('emergency-contact/', EmergencyContactListView.as_view(), name='emergecy-contact-list'),
]
