from rest_framework import routers
from django.urls import path, include
from user_control.views import *

#from .views import UserView, current_user
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


router = routers.DefaultRouter()
router.register(r'register', UserView, basename='register')

# Sin usar router para estas views "manuales"
# urlpatterns = [
#     path('register/', include(router.urls)),
#     path('login/', views.LoginView.as_view(), name='login'),
#     path('logout/', views.LogoutView.as_view(), name='logout'),
#     path('admin/create-user/', views.CreateUserByAdminView.as_view(), name='admin-create-user'),
#     path('admin/create-branch/', views.CreateBranchByAdminView.as_view(), name='admin-create-branch'),
# ]

urlpatterns = [
    #path('', include(router.urls)),  # incluye las rutas de UserView
    path('register/', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('logout/', LogoutView.as_view(), name='logout'),
    #path('me/', current_user, name='current_user'),
]
