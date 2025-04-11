from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import User

# Sin usar router para estas views "manuales"
urlpatterns = [
    path('register/', User.as_view(), name='register'),
    # path('login/', User.as_view(), name='login'),
    # path('logout/', User.as_view(), name='logout'),
    # path('me/', User, name='current_user'),
]