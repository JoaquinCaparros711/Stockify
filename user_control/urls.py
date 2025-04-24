from rest_framework.routers import DefaultRouter
from rest_framework import routers
from django.urls import path, include
from user_control import views
from user_control import views

router = routers.DefaultRouter()
router.register(r'register', views.UserView, basename='register')

# Sin usar router para estas views "manuales"
urlpatterns = [
    path('register/', include(router.urls)),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('admin/create-user/', views.CreateUserByAdminView.as_view(), name='admin-create-user'),
    path('admin/create-branch/', views.CreateBranchByAdminView.as_view(), name='admin-create-branch'),
]