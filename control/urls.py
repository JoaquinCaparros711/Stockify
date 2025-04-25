from django.urls import path, include 
from rest_framework import routers
from control import views


router = routers.DefaultRouter()
router.register(r'company', views.CompanyView, basename='company')
# router.register(r'branch', views.BranchView, basename='branch')
# router.register(r'user', views.UserView, basename='user')
router.register(r'product', views.ProductView, basename='product')
router.register(r'branch_stock', views.BranchStockView, basename='branch_stock')
router.register(r'stock_movement', views.StockMovementView, basename='stock_movement')


urlpatterns = [
    path('control/model/', include(router.urls))
]