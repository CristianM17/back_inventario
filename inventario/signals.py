from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import IngresoProducto

@receiver(post_save, sender=IngresoProducto)
def my_handler(sender, **kwargs):
    print("Se creo algo")