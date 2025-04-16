from rest_framework.routers import DefaultRouter
from rest_framework import routers
from django.urls import path, include
from user_control import views

router = routers.DefaultRouter()
router.register(r'register', views.UserView, basename='register')

# Sin usar router para estas views "manuales"
urlpatterns = [
    path('register/', include(router.urls))
]