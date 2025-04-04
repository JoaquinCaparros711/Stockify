from django.urls import path, include 
from rest_framework import routers
from control import views


router = routers.DefaultRouter()
router.register(r'company', views.CompanyView, basename='company')
router.register(r'branch', views.BranchView, basename='branch')
router.register(r'user', views.UserView, basename='user')
router.register(r'product', views.ProductView, basename='product')
router.register(r'branch_stock', views.BranchStockView, basename='BranchStock')
router.register(r'stock_movement', views.StockMovementView, basename='StockMovement')


urlpatterns = [
    path('control/model/', include(router.urls))
]