from django.db import models

# Create your models here.
STATUS_CHOICES=(("pending","pending"),("paid","paid"),("overdue","overdue"))

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return self.name
    

class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    issue_date = models.DateField()
    due_date = models.DateField()
    status=models.CharField(max_length=100,choices=STATUS_CHOICES,null=True,default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
      return f"Invoice #{self.id}"
    
  
  
class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Invoice #{self.id}"
