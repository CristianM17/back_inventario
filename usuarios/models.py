from django.db import models
from django.conf import settings

# Create your models here.
class DatosComplementarios(models.Model):
    """ 
    Modelo que se relaciona con auth_users, para complementar los datos del usuario que seria
    la empresa que usa la plataforma de inventario
    """
    razon_social = models.CharField(
        'Razon_social', max_length=60, null=False, unique=True, help_text= "Agregar el nombre de la empresa"
    )
    nit = models.PositiveIntegerField(
        'NIT', unique=True, null=False, help_text="Agregar el nit de la empresa sin el codigo de verificacion y sin puntos"
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,on_delete=models.CASCADE, help_text="Relacion con la tabla auth_user"
    )
    direccion = models.CharField(
        'Direccion', max_length=255, null=False, help_text="Dirección donde se encuentra la empresa"
    )
    pais = models.CharField(
        'Pais', max_length=60, help_text="Pais donde se encuentra la empresa"
    )
    ubicacion = models.CharField(
        'Ubicacion', max_length=60, null=False,help_text="Hace referencia en que ciudad se encuentra la empresa"
    )
    telefono = models.BigIntegerField(
        'Telefono',unique=True, null=False,help_text="Numero de contacto a la que se puede llamar a la empresa"
    )
    pagina_web = models.URLField(
        'Pagina_web', max_length=200, unique=True, null=True, blank=True,help_text="Pagina web de la empresa"
    )
    
    
    class Meta:
        db_table = "datos_complementarios"
        db_table_comment = "Tabla que complementa los datos de un usuario registrado, con datos adiccionales al de la tabla auth_user"
        ordering = ["razon_social"]
        
    def __str__(self):
        return f" {self.razon_social} - {self.nit}"