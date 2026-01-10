from django.utils import timezone

from django.db import models
from django.forms import CharField
from django.urls import reverse

from shop.settings import AUTH_USER_MODEL

# Create your models here.

"""
product
-nom
-prix
-quantite en stock
-description
-image
"""

class product(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    price = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to="products", blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.stock})"

    def get_absolute_url(self):
        return reverse("product", kwargs={"slug": self.slug})

# Article (Order)
"""
-utilisateur
-produit
-quantite
-commande ou non
"""
class Order(models.Model):
     user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
     product = models.ForeignKey(product, on_delete=models.CASCADE)
     quantity = models.IntegerField(default=1)
     ordered = models.BooleanField(default=False)
     ordered_date = models.DateTimeField(blank=True, null=True)

     def __str__(self):
         return f"{self.product.name} ({self.quantity})"

# Panier (Cart)
"""
-utilisateur
-article
-commande ou non
-date de la commande
"""

class Cart(models.Model):
    user = models.OneToOneField( AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        for order in self.orders.all():
            order.ordered = True
            order.ordered_date = timezone.now()
            order.save()

        self.orders.clear()
        super().delete(*args, **kwargs)

#Electronique

class Electronique(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    price = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to="electronique", blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("electronique-detail", kwargs={"slug": self.slug})

class Order_electronique(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    Electronique = models.ForeignKey(Electronique, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.Electronique.name} ({self.quantity})"

class Cart_electronique(models.Model):
    user = models.OneToOneField( AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order_electronique)

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        for order in self.orders.all():
            order.ordered = True
            order.ordered_date = timezone.now()
            order.save()

        self.orders.clear()
        super().delete(*args, **kwargs)

#Cosmetique

class Cosmetique(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    price = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to="cosmetiques", blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("cosmetique-detail", kwargs={"slug": self.slug})

class Order_cosmetique(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    Cosmetique = models.ForeignKey(Cosmetique, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.Cosmetique.name} ({self.quantity})"

class Cart_cosmetique(models.Model):
    user = models.OneToOneField( AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order_cosmetique)

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        for order in self.orders.all():
            order.ordered = True
            order.ordered_date = timezone.now()
            order.save()

        self.orders.clear()
        super().delete(*args, **kwargs)

#Bijoux

class Bijoux(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    price = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to="bijoux", blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("bijoux-detail", kwargs={"slug": self.slug})

class Order_bijoux(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    Bijoux = models.ForeignKey(Bijoux, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.Bijoux.name} ({self.quantity})"

class Cart_bijoux(models.Model):
    user = models.OneToOneField( AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order_bijoux)

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        for order in self.orders.all():
            order.ordered = True
            order.ordered_date = timezone.now()
            order.save()

        self.orders.clear()
        super().delete(*args, **kwargs)


class Payment(models.Model):
    amount = models.IntegerField()
    stripe_charge_id = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    bijoux_name = models.CharField(max_length=128, blank=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"Paiement de {self.amount} centimes pour {self.bijoux_name}, ID : {self.stripe_charge_id}"

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email







