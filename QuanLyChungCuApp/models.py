from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Quản trị viên'),
        ('resident', 'Cư dân'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='resident')
    avatar = CloudinaryField('avatar', null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    profile_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.role})"


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fee_type = models.CharField(max_length=50, choices=[('management', 'Phí quản lý'), ('parking', 'Phí gửi xe'), ('other', 'Dịch vụ khác')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=[('momo_upload', 'Momo chuyển khoản'), ('momo_gateway', 'Momo gateway'), ('vnpay', 'VNPAY')])
    receipt_image = models.ImageField(upload_to='payments/', null=True, blank=True)  # Uỷ nhiệm chi
    timestamp = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)


class RelativeAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=20)
    relation = models.CharField(max_length=50)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

