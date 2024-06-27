from django.urls import path
from .views import AdultHeartRateView, ChildHeartRateView

urlpatterns = [
    path("heartrates/adult", AdultHeartRateView.as_view(), name="heartrates-aduld"),
    path("heartrates/child", ChildHeartRateView.as_view(), name="heartrates-child"),
]
