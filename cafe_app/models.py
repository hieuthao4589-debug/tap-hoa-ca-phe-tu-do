from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên danh mục")

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Danh mục"
    )
    name = models.CharField(max_length=200, verbose_name="Tên món")
    price = models.IntegerField(verbose_name="Giá tiền")
    image = models.ImageField(
        upload_to="products/", null=True, blank=True, verbose_name="Hình ảnh"
    )

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = (
        ("Pending", "Đang chờ xử lý"),
        ("Processing", "Đang pha chế"),
        ("Completed", "Đã hoàn thành"),
        ("Cancelled", "Đã hủy"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    total_price = models.IntegerField(default=0)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Đơn hàng #{self.id} - {self.total_price}đ"


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="details")
    product_name = models.CharField(max_length=200)
    size = models.CharField(max_length=50, blank=True, null=True)
    ice = models.CharField(max_length=50, blank=True, null=True)
    sweetness = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()

    def __str__(self):
        return f"{self.quantity}x {self.product_name}"


class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sizes")
    name = models.CharField(
        max_length=50, help_text="Ví dụ: 360ml, 500ml, 700ml, Standard..."
    )
    price = models.IntegerField(help_text="Giá tiền cho size này")

    def __str__(self):
        return f"{self.product.name} - {self.name} ({self.price}đ)"


from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Profile của {self.user.username}"
