from django.urls import path
from .views import AdultHeartRateView, ChildHeartRateView, SendHeartRateView

urlpatterns = [
    path("heartrates/adult", AdultHeartRateView.as_view(), name="heartrates-aduld"),
    path("heartrates/child", ChildHeartRateView.as_view(), name="heartrates-child"),
    path("heartrates/send", SendHeartRateView.as_view(), name="heartrates-send"),
]
