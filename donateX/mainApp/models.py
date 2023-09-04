from django.db import models
from django.contrib.auth.models import AbstractUser


class Donation(models.Model):
    donor_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    # Add more fields as needed for your use case


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, unique=True)
    
    # Add related_name to avoid clashes with default User model
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users',
        blank=True,
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return self.username
    
class PaymentHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.donation.donor_name}'