from rest_framework import serializers
from .models import Customer, Product, Order, OrderItem
from django.db import transaction
from decimal import Decimal
from django.db.models import F, Sum

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'joined_on']
        read_only_fields = ['id', 'joined_on']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']
        read_only_fields = ['id']

class OrderItemSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_detail', 'quantity']
        read_only_fields = ['id', 'product_detail']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    customer_detail = CustomerSerializer(source='customer', read_only=True)
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), write_only=True)
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_detail', 'order_date', 'items', 'total_price']
        read_only_fields = ['id', 'order_date', 'total_price', 'customer_detail']

    def validate_items(self, value):
        if not value or len(value) == 0:
            raise serializers.ValidationError("An order must have at least one item.")
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            order_items = []
            for item in items_data:
                product = item['product']
                quantity = item.get('quantity', 1)
                if quantity < 1:
                    raise serializers.ValidationError("Quantity must be >= 1.")
                oi = OrderItem(order=order, product=product, quantity=quantity)
                order_items.append(oi)
            OrderItem.objects.bulk_create(order_items)
            # annotate total price for response (optional; serializer's to_representation will re-query)
            return order

    def to_representation(self, instance):
        # annotate total price on instance to avoid N+1 in list view where possible
        rep = super().to_representation(instance)
        total = instance.items.aggregate(
            total=Sum(F('quantity') * F('product__price'))
        )['total'] or Decimal('0.00')
        rep['total_price'] = "%.2f" % (total)
        return rep
