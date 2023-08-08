from django.db import models
from django.conf import settings


class CatalogItem(models.Model):
    title: str = models.CharField(max_length=50, blank=False, null=False)
    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="subcategories",
    )

    class Meta:
        verbose_name = "CatalogItem"
        verbose_name_plural = "CatalogItem"
        ordering = ["pk"]

    def __str__(self):
        return f"{self.title}"


def path_image_catalog_item(instance: "ImageCatalogItem", filename: str) -> str:
    return "categories/category_{title}/{filename}".format(
        title=instance.catalog_item.title,
        filename=filename,
    )


class ImageCatalogItem(models.Model):
    catalog_item = models.OneToOneField(
        CatalogItem, on_delete=models.CASCADE, related_name="image"
    )
    image = models.ImageField(null=True, blank=True, upload_to=path_image_catalog_item)

    class Meta:
        verbose_name = "CatalogItemImage"
        verbose_name_plural = "CatalogItemImages"
        ordering = ["pk"]

    def src(self):
        return f"{settings.MEDIA_URL}{self.image}"

    def alt(self):
        return f"{self.catalog_item.title}_image"

    def __str__(self) -> str:
        return f"{self.catalog_item.title}_image"


class Product(models.Model):
    category = models.ForeignKey(
        CatalogItem, on_delete=models.SET_NULL, null=True, related_name="products"
    )
    title = models.CharField(max_length=128, null=False, blank=False)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2, null=False)
    count = models.IntegerField(default=0, null=False)
    date = models.DateTimeField(auto_now_add=True, null=False)
    description = models.CharField(max_length=256, null=True, blank=True)
    freeDelivery = models.BooleanField(default=True)
    rating = models.DecimalField(default=0, max_digits=3, decimal_places=2, null=False)
    # ProductFull
    fullDescription = models.TextField(null=False, blank=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["pk"]

    def __str__(self):
        return self.title


def path_image_product(instanse: "ImageProduct", filename):
    return "products/{title}/{filename}".format(
        title=instanse.product.title,
        filename=filename,
    )


class ImageProduct(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.FileField(null=True, blank=True, upload_to=path_image_product)

    class Meta:
        verbose_name = "ProductImage"
        verbose_name_plural = "ProductImages"
        ordering = ["pk"]

    def src(self):
        return f"{settings.MEDIA_URL}{self.image}"

    def alt(self):
        return f"{self.product.title}_image"

    def __str__(self) -> str:
        return f"{self.product.title}_image"


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    author = models.CharField(max_length=32)
    email = models.EmailField(max_length=256)
    text = models.TextField(default="")
    rate = models.PositiveSmallIntegerField(blank=False, default=5)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ["pk"]

    def __str__(self):
        return f"{self.author} - {self.product.title}"


class Specification(models.Model):
    product = models.ManyToManyField(Product, related_name="specifications")
    name = models.CharField(max_length=256, default="")
    value = models.CharField(max_length=256, default="")

    class Meta:
        verbose_name = "Specification"
        verbose_name_plural = "Specifications"
        ordering = ["pk"]

    def __str__(self):
        return self.name


class Tag(models.Model):
    product = models.ManyToManyField(Product, related_name="tags")
    name = models.CharField(max_length=32, default="")

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["pk"]

    def __str__(self):
        return self.name


class Sale(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="sales"
    )
    salePrice = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    dateFrom = models.DateField(blank=True, null=True)
    dateTo = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Sale"
        verbose_name_plural = "Sales"

    def price(self):
        return self.product.price

    def title(self):
        return self.product.title

    def images(self):
        return self.product.images

    def href(self):
        return f"/product/{self.product.pk}"

    def __str__(self):
        return self.product.title
