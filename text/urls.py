from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name="homepage"),
    path('notfound', views.NotFoundView.as_view(), name="notfound")
]
