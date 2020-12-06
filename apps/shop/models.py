from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType


User = get_user_model()

# category
# product
# product_in_cart
# cart
# order
# buyer
# product_description
# ********


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name = "Категория")
    slug = models.SlugField(verbose_name='URL', unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name = "Продукт")
    slug = models.SlugField(verbose_name='URL', unique=True)
    image = models.ImageField(verbose_name='Картинка', upload_to=None, height_field=None, width_field=None, max_length=None)
    description = models.TextField(verbose_name="Описание", null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return self.title

class Product_in_Cart(models.Model):
    buyer = models.ForeignKey("Customer", verbose_name="Покупатель", on_delete=models.CASCADE)
    cart = models.ForeignKey("Cart", verbose_name="Корзина", on_delete=models.CASCADE, 
                            related_name = "related products")
    product = models.ForeignKey(Product, verbose_name="Товар", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена всего")

    def __str__(self):
        return f"Продукт: {self.product.title} для корзины"

class Cart(models.Model):
    owner = models.ForeignKey("Customer", verbose_name="Владелец", on_delete=models.CASCADE)
    products = models.ManyToManyField(Product_in_Cart, blank=True, related_name="related cart")
    total_products = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена итого")

    def __str__(self):
        return self.owner

class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    address = models.CharField(max_length=255, verbose_name="Адрес")

    def __str__(self):
        return f"Покупатель {self.user.first_name} {self.user.last_name}"

class Product_description(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    product_name = models.CharField(max_length=255, verbose_name="Товар для описания")

    def __str__(self):
        return f"Описание товара {self.product_name}"
    
