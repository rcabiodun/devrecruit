# from django.shortcuts import render
# from django.http import HttpResponse
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from rest_framework import status
# from .models import *
# from .serializers import *

# @api_view(['GET'])
# def get_customers(request):
#     """
#     Retrieve all customers from the database
    
#     Endpoint: GET /customers/
#     Returns:
#         200: List of all customers with their details
#     """
#     customers = Customer.objects.all()  # Fetch all customer records
#     serializer = CustomerSerializer(customers, many=True)  # Serialize multiple customers
#     return Response(serializer.data, status=status.HTTP_200_OK)

# @api_view(['GET'])
# def get_customer(request, pk):
#     """
#     Retrieve a specific customer by their ID
    
#     Endpoint: GET /customers/<pk>/
#     Args:
#         pk: Primary key (ID) of the customer
#     Returns:
#         200: Customer details if found
#         404: Error message if customer doesn't exist
#     """
#     try:
#         customer = Customer.objects.get(pk=pk)  # Attempt to fetch customer by ID
#     except Customer.DoesNotExist:
#         return Response(
#             {'message': 'Customer not found'}, 
#             status=status.HTTP_404_NOT_FOUND
#         )
#     serializer = CustomerSerializer(customer)  # Serialize single customer
#     return Response(serializer.data, status=status.HTTP_200_OK)

# @api_view(['POST'])
# def create_customer(request):
#     """
#     Create a new customer
    
#     Endpoint: POST /customers/
#     Request Body:
#         - name: Customer name
#         - email: Customer email
#     Returns:
#         201: Newly created customer details
#         400: Validation errors if request data is invalid
#     """
#     serializer = CustomerSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()  # Save new customer to database
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def create_invoice(request):
#     """
#     Create a new invoice for a customer
    
#     Endpoint: POST /invoices/
#     Request Body:
#         - customer: Customer ID
#         - issue_date: Date invoice is issued
#         - due_date: Payment due date
#         - items: List of invoice items (optional)
#     Returns:
#         201: Newly created invoice details
#         404: Error if customer not found
#         400: Validation errors if request data is invalid
#     """
#     # Verify customer exists before creating invoice
#     customer_id = request.data.get("customer")
#     try:
#         customer = Customer.objects.get(pk=customer_id)
#     except Customer.DoesNotExist:
#         return Response(
#             {'message': 'Customer not found'}, 
#             status=status.HTTP_404_NOT_FOUND
#         )
    
#     # Create invoice with validated data
#     serializer = InvoiceSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def get_invoices(request, pk):
#     """
#     Retrieve a specific invoice by its ID
    
#     Endpoint: GET /invoices/<pk>/
#     Args:
#         pk: Primary key (ID) of the invoice
#     Returns:
#         200: Invoice details including items if found
#         404: Error message if invoice doesn't exist
#     """
#     try:
#         invoice = Invoice.objects.get(pk=pk)  # Attempt to fetch invoice by ID
#         serializer = InvoiceSerializer(invoice)  # Serialize invoice with nested items
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     except Invoice.DoesNotExist:
#         return Response(
#             {'message': 'Invoice not found'}, 
#             status=status.HTTP_404_NOT_FOUND
#         )

# @api_view(['PATCH'])
# def update_invoice_status(request, pk):
#     """
#     Update the status of an existing invoice
    
#     Endpoint: PATCH /invoices/<pk>/status/
#     Args:
#         pk: Primary key (ID) of the invoice
#     Request Body:
#         - status: New status value (must be one of: pending, paid, overdue)
#     Returns:
#         200: Updated invoice details
#         404: Error if invoice not found
#         400: Error if status value is invalid
#     """
#     try:
#         invoice = Invoice.objects.get(pk=pk)  # Fetch invoice to update
#     except Invoice.DoesNotExist:
#         return Response(
#             {'message': 'Invoice not found'}, 
#             status=status.HTTP_404_NOT_FOUND
#         )
    
#     # Validate status value
#     status_value = request.data.get('status')
#     if not status_value or status_value not in dict(STATUS_CHOICES):
#         return Response(
#             {'message': 'Invalid status. Must be one of: pending, paid, overdue'}, 
#             status=status.HTTP_400_BAD_REQUEST
#         )
    
#     # Update and save invoice status
#     invoice.status = status_value
#     invoice.save()
    
#     serializer = InvoiceSerializer(invoice)
#     return Response(serializer.data, status=status.HTTP_200_OK)  # Serialize and return updated invoice

