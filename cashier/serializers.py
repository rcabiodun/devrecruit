from rest_framework import serializers
from .models import Customer, Invoice, InvoiceItem
from django.db.models import Sum 

# Serializer for Customer model - handles conversion between Customer model instances and JSON
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'  # Serializes all fields defined in the Customer model

# Serializer for InvoiceItem model - handles individual items within an invoice
class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = '__all__'  # Includes all fields: invoice, description, quantity, unit_price, total

# Main Invoice serializer - handles the complete invoice including nested items
class InvoiceSerializer(serializers.ModelSerializer):
    # Nested serializer for invoice items - allows handling multiple items per invoice
    # many=True indicates this is a one-to-many relationship
    # required=False means items can be empty when creating/updating an invoice
    items = InvoiceItemSerializer(many=True, required=False)
    
    # Dynamic field that calculates the total amount of the invoice
    # Uses get_total method defined below to compute the value
    total = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = '__all__'  # Includes all fields from Invoice model plus 'items' and 'total'
    
    def validate(self, data):
        """
        Object-level validation method
        Ensures the due_date is chronologically after the issue_date
        Args:
            data: Dictionary of field values to validate
        Returns:
            Validated data if validation passes
        Raises:
            ValidationError if due_date is before issue_date
        """
        if data['due_date'] < data['issue_date']:
            raise serializers.ValidationError("Due date must be after issue date")
        return data

    def validate_issue_date(self, value):
        """
        Field-level validation for issue_date
        Ensures the issue_date is not in the past
        Args:
            value: The issue_date value to validate
        Returns:
            Validated value if validation passes
        Raises:
            ValidationError if issue_date is in the past
        """
        from django.utils import timezone
        if value < timezone.now().date():
            raise serializers.ValidationError("Issue date cannot be in the past")
        return value
 
    def create(self, validated_data):
        """
        Custom create method to handle nested invoice items
        Args:
            validated_data: Dictionary containing validated invoice and items data
        Returns:
            Created Invoice instance
        Raises:
            ValidationError if no items are provided
        """
        # Extract items data from validated_data to handle separately
        items_data = validated_data.pop('items', [])
        if len(items_data) == 0:
            raise serializers.ValidationError("Invoice must have at least one item")
        
        # Create the invoice instance first
        invoice = super().create(validated_data)
        
        # Create associated invoice items
        for item_data in items_data:
            item_data['invoice'] = invoice  # Link item to the invoice
            # Calculate total for individual item
            item_data['total'] = item_data['quantity'] * item_data['unit_price']
            InvoiceItem.objects.create(**item_data)
        
        return invoice

    def get_total(self, obj):
        """
        Method to calculate the total amount of the invoice
        Used by the SerializerMethodField 'total'
        Args:
            obj: Invoice instance
        Returns:
            Total amount of all invoice items combined
        """
        # Use Django's aggregate function to sum the total field of all related items
        total = obj.items.aggregate(total=Sum('total'))['total']
        return total
    
