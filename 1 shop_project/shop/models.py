from django.db import models
from django.core.validators import MinValueValidator, MinLengthValidator


class TimeStampMixin(models.Model):
    # برای سادگی تعریف شده.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampMixin):
    # برای سادگی به خودش فارین کی نزده.
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.title}"


class Discount(TimeStampMixin):
    # برای سادگی مثل شیرینی فروشی نیست و فقط مقداری تعریف شده.
    amount = models.FloatField(validators=[MinValueValidator(0)])
    code = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        if self.description:
            return f"{self.description} (amount: {self.amount})"
        else:
            return f"discount amount: {self.amount}"


class Product(TimeStampMixin):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products"
    )
    description = models.TextField()
    slug = models.SlugField(allow_unicode=True)
    # اول قرار بود دلاری باشه. بعد که اسم استان ها رو فارسی نوشتم و گروه ها رو
    # این رو هم عوض کردم. ولی اینتیجر نذاشتم و مکس دیجیتس رو ۱۵ کردم 😁
    price = models.DecimalField(max_digits=15, decimal_places=2)
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    discounts = models.ManyToManyField(Discount, blank=True)

    def __str__(self):
        return f"{self.title}: {self.price}"


class Comment(TimeStampMixin):
    COMMENT_STATUS_WAITING = "w"
    COMMENT_STATUS_APPROVED = "a"
    COMMENT_STATUS_REJECTED = "r"
    COMMENT_STATUS_CHOICES = [
        (COMMENT_STATUS_WAITING, "Waiting"),
        (COMMENT_STATUS_APPROVED, "Approved"),
        (COMMENT_STATUS_REJECTED, "Rejected"),
    ]

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="comments"
    )
    # میتونست به یوزرها وصل بشه. اما برای سادگی نکردم.
    name = models.CharField(max_length=255)
    text = models.TextField(max_length=5000, validators=[MinLengthValidator(10)])
    status = models.CharField(
        max_length=1, choices=COMMENT_STATUS_CHOICES, default=COMMENT_STATUS_WAITING
    )

    def __str__(self):
        return f"{self.name}: {self.text[:30]}"


class Customer(TimeStampMixin):
    # برای سادگی به یوزرها وصلش نکردم.
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Country(TimeStampMixin):
    # name = models.CharField(max_length=255, unique=True) بگم که واقعی این شکلیه اما برای سادگی برداشتم و این خط رو حذف کنم.
    # برای تو در تو نوشتن سریالایزرها کشور و استان و شهر رو این شکلی نوشتم که هم تو در تو باشه هم ساده
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Province(TimeStampMixin):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name}"


class City(TimeStampMixin):
    name = models.CharField(max_length=255)
    province = models.ForeignKey(Province, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name}"


class Address(TimeStampMixin):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="addresses"
    )
    city = models.ForeignKey(City, on_delete= models.PROTECT, related_name="addresses")
    street = models.CharField(max_length=255)
    alley = models.CharField(max_length=255)
    building_number = models.SmallIntegerField(validators=[MinValueValidator(1)])
    building_name = models.CharField(max_length=255, blank=True)
    floor = models.SmallIntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    unit = models.SmallIntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    zip_code = models.CharField(max_length=10, null=True, blank=True, validators=[MinLengthValidator(10)])

    def __str__(self):
        return f"{self.street} - {self.alley} - {self.building_number} - {self.building_name}"
        return f"{self.city} - {self.street} - {self.alley} - {self.building_number} - {self.building_name}"


class Basket(TimeStampMixin):
    pass


class BasketItem(TimeStampMixin):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="basket_items"
    )
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["basket", "product"],
                name="unique_basket_product"
            )
        ]
    # یادآوری دیپریکیشن
    # class Meta:
    #     unique_together = [["basket", "product"]]

    def __str__(self):
        return f"{self.product} - (quantity: {self.quantity})"


class Order(TimeStampMixin):
    ORDER_STATUS_PAID = "p"
    ORDER_STATUS_UNPAID = "u"
    ORDER_STATUS_CANCELED = "c"
    ORDER_STATUS_CHOICES = [
        (ORDER_STATUS_PAID, "Paid"),
        (ORDER_STATUS_UNPAID, "Unpaid"),
        (ORDER_STATUS_CANCELED, "Canceled"),
    ]

    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name="orders"
    )
    status = models.CharField(
        max_length=1, choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS_UNPAID
    )

    def __str__(self):
        return f"Order of {self.customer} (Status: {self.get_status_display()})"


class OrderItem(TimeStampMixin):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="order_items"
    )
    quantity = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["order", "product"],
                name="unique_order_product"
            )
        ]
    
    def __str__(self):
        return f"{self.product} - (quantity: {self.quantity})"
