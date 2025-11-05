from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Customer, Product, Order, OrderItem
from decimal import Decimal

class AnalyticsTests(APITestCase):
    def setUp(self):
        # create customers
        self.c1 = Customer.objects.create(name='Alice', email='alice@example.com')
        self.c2 = Customer.objects.create(name='Bob', email='bob@example.com')

        # products
        self.p1 = Product.objects.create(name='Widget', price=Decimal('10.00'))
        self.p2 = Product.objects.create(name='Gadget', price=Decimal('5.00'))

        # order 1: Alice buys 2 widgets
        o1 = Order.objects.create(customer=self.c1)
        OrderItem.objects.create(order=o1, product=self.p1, quantity=2)

        # order 2: Bob buys 3 gadgets
        o2 = Order.objects.create(customer=self.c2)
        OrderItem.objects.create(order=o2, product=self.p2, quantity=3)

    def test_sales_summary(self):
        url = reverse('sales-summary')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        # total sales = 2*10 + 3*5 = 35
        self.assertEqual(data['total_sales'], '35.00')
        self.assertEqual(data['total_customers'], 2)
        self.assertEqual(int(data['total_products_sold']), 5)
