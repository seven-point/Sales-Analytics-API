from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Customer, Product, Order, OrderItem
from .serializers import (
    CustomerSerializer, ProductSerializer,
    OrderSerializer
)
from django.db.models import Sum, F, Value
from django.db.models.functions import Coalesce
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.utils.dateparse import parse_date
from django.db.models import DecimalField, ExpressionWrapper
from django.db.models import Count
from django.shortcuts import get_object_or_404

# Customers
class CustomerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Customer.objects.all().order_by('-joined_on')
    serializer_class = CustomerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email']

# Products
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter,]
    search_fields = ['name']

# Orders
class OrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.select_related('customer').prefetch_related('items__product').all().order_by('-order_date')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# Analytics helpers
def _parse_date_range(request):
    from_date = request.query_params.get('from')
    to_date = request.query_params.get('to')
    parsed = {}
    if from_date:
        d = parse_date(from_date)
        if d:
            parsed['from'] = d
    if to_date:
        d = parse_date(to_date)
        if d:
            parsed['to'] = d
    return parsed

# Sales summary
class SalesSummaryAPIView(views.APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        dr = _parse_date_range(request)
        items = OrderItem.objects.select_related('order', 'product', 'order__customer')
        if 'from' in dr:
            items = items.filter(order__order_date__date__gte=dr['from'])
        if 'to' in dr:
            items = items.filter(order__order_date__date__lte=dr['to'])

        total_sales = items.aggregate(
            total=Coalesce(Sum(F('quantity') * F('product__price')), 0)
        )['total']

        total_customers = Customer.objects.count()
        total_products_sold = items.aggregate(total_qty=Coalesce(Sum('quantity'), 0))['total_qty']

        return Response({
            'total_sales': "%.2f" % (total_sales or 0),
            'total_customers': total_customers,
            'total_products_sold': int(total_products_sold or 0),
        })

# Top customers by purchase amount
class TopCustomersAPIView(views.APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        dr = _parse_date_range(request)
        items = OrderItem.objects.select_related('order', 'product', 'order__customer')
        if 'from' in dr:
            items = items.filter(order__order_date__date__gte=dr['from'])
        if 'to' in dr:
            items = items.filter(order__order_date__date__lte=dr['to'])

        # group by customer, sum quantity*price
        qs = items.values('order__customer', 'order__customer__name', 'order__customer__email').annotate(
            total_spent=Coalesce(Sum(F('quantity') * F('product__price')), 0)
        ).order_by('-total_spent')[:5]

        results = [
            {
                'customer_id': r['order__customer'],
                'name': r['order__customer__name'],
                'email': r['order__customer__email'],
                'total_spent': "%.2f" % (r['total_spent'] or 0)
            } for r in qs
        ]
        return Response(results)

# Top products by quantity sold
class TopProductsAPIView(views.APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        dr = _parse_date_range(request)
        items = OrderItem.objects.select_related('product', 'order')
        if 'from' in dr:
            items = items.filter(order__order_date__date__gte=dr['from'])
        if 'to' in dr:
            items = items.filter(order__order_date__date__lte=dr['to'])

        qs = items.values('product', 'product__name').annotate(
            sold_qty=Coalesce(Sum('quantity'), 0)
        ).order_by('-sold_qty')[:5]

        results = [
            {
                'product_id': r['product'],
                'name': r['product__name'],
                'sold_qty': int(r['sold_qty'] or 0)
            } for r in qs
        ]
        return Response(results)
