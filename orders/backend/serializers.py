from rest_framework import serializers
from backend import models


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contact
        fields = ('user_id', 'full_name', 'phone_number', 'address')
        read_only_fields = ('id',)
        extra_kwargs = {
            'user': {'write_only': True},
        }          


class UserSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(read_only=True, many=True)

    class Meta:
        model = models.User
        fields = ('id', 'full_name', 'email', 'company', 'position', 'contacts', 'is_staff', 'is_superuser')
        read_only_fields = ('id', 'is_staff', 'is_superuser')


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Shop
        fields = ('id', 'name, work_email')
        read_only_fields = ('id',)


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Parameter
        fields = ('id', 'name', )
        read_only_fields = ('id',)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ('id', 'name', )
        read_only_fields = ('id',)


class ProductParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductParameter
        fields = ('product_id', 'parameter_id', 'value')


class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Catalog
        fields = ('category', 'product_id', 'shop_id', 'price', 'qty', 'on_sale')
    

class OrderlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Orderlist
        fields = ('order_id', 'product_id', 'shop_id', 'current_price', 'qty', 'coast')
        # read_only_fields = ('id',)
        extra_kwargs = {
            'order_id': {'write_only': True}
        }

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ('id', 'user_id', 'date', 'status', 'total_cost')
        read_only_fields = ('id',)

                          