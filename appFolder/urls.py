from django.urls import path
from . import views

# url configuration for this app. Import this in the main url page.
urlpatterns = [
    path('page1/', views.page1)
]