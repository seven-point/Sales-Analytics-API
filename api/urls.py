from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    # Auth (bonus)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # core endpoints
    path('customers/', views.CustomerListCreateAPIView.as_view(), name='customer-list-create'),
    path('products/', views.ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('orders/', views.OrderListCreateAPIView.as_view(), name='order-list-create'),

    # analytics
    path('analytics/sales-summary/', views.SalesSummaryAPIView.as_view(), name='sales-summary'),
    path('analytics/top-customers/', views.TopCustomersAPIView.as_view(), name='top-customers'),
    path('analytics/top-products/', views.TopProductsAPIView.as_view(), name='top-products'),
]
