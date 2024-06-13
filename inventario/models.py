from django.db import models
from django.db.models import Q
from django.db.models.functions import Length
import pgtrigger

# Create your models here.
class Fabricante(models.Model):
    razon_social = models.CharField(
        'Razon_social', max_length=60, null=False, unique=True, help_text= "Agregar el nombre de la empresa"
    )
    nit = models.PositiveIntegerField(
        'NIT', unique=True, null=False, help_text="Agregar el nit de la empresa sin el codigo de verificacion y sin puntos"
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
    correo = models.EmailField(
        "Correo_electronico", max_length=254, null=False, unique=True, help_text="Correo electronico de contacto del fabricante"
    )
    pagina_web = models.URLField(
        'Pagina_web', max_length=200, unique=True, null=True, blank=True,help_text="Pagina web de la empresa"
    )
    
    
    class Meta:
        db_table = "fabricante"
        verbose_name_plural = "Fabricantes"
        db_table_comment = "Tabla donde iran los datos de un fabricante"
        ordering = ["razon_social"]
        
        
    def __str__(self):
        return f"{self.razon_social} - {self.nit}"
    
    
class Producto(models.Model):
    
    categoria_opciones = [
        ('CEL', 'Celulares'),
        ('PC', 'computadores'),
        ('ELEC', 'Electrodomésticos'),
        ('ALIM', 'Alimentos'),
        ('ACC', 'Accesorios'),
        ('VID', 'Videojuegos'),
        ('AUD', 'Audio'),
        ('CAM', 'Cámaras'),
        ('HOG', 'Hogar'),
        ('DEP', 'Deportes'),
        ('JUG', 'Juguetes'),
        ('OT', 'Otros'),
    ]
    
    sku = models.CharField(
        'SKU', max_length=255, primary_key=True, help_text='codigo de identificación unica para el producto'
    )
    nombre = models.CharField(
        'Nombre', max_length=255, null=False, unique=True, help_text='nombre que tiene el producto'
    )
    imagen = models.ImageField('Imagen_producto',blank='', default="", upload_to='imgProductos/', help_text='Imagen del producto')
    descripcion = models.TextField(
        'Descripcion', null=False, help_text='Descripcion que pueda tener el producto que se vean relevantes'
    )
    precio = models.DecimalField(
        "precio",null=False, max_digits=15, decimal_places=2, help_text='precio unitario del producto, la moneda que se maneja por defecto es el peso colombiano'
    )
    stock_actual = models.PositiveIntegerField(
        'Stock_actual' ,null=False, default=0, help_text='Cantidad actual del prodcuto'
    )
    fabricante = models.ForeignKey(Fabricante, related_name="producto_fabricante",on_delete=models.CASCADE
    )
    categoria = models.CharField(
        "Categorias", max_length=4, choices=categoria_opciones, help_text='Categorias en las que pertenecen los productos'
    )
    fecha_creacion = models.DateTimeField(
        'Fecha_creación', auto_now_add=True
    )
    fecha_actualizacion_stock = models.DateTimeField(
        'Fecha_actualización',auto_now=True
    )
    is_active = models.BooleanField(
        default=True,null=False, help_text='Determina si el producto esta activo para vender'
    )

    class Meta:
        db_table = "producto"
        verbose_name_plural = "Productos"
        db_table_comment = "Tabla donde iran los productos"
        order_with_respect_to = "fabricante_id" #ideal con campos FK
        
    def __str__(self):
        return f"{self.nombre} - {self.sku}"


class Cliente(models.Model):
    tipo_identificacion_opciones = [
        ('CC', 'Cedula de Ciudadania'),
        ('CE', 'Cedula de Extranjeria'),
        ('PPT', 'Permiso por Protección Personal'),
        ('NIT', 'Nit'),
        ('PS', 'Pasaporte'),
    ]
    
    primer_nombre = models.CharField("Primer_nombre", max_length=50, null=False)
    segundo_nombre = models.CharField("Segundo_nombre", max_length=50, blank=True)
    primer_apellido = models.CharField("Primer_apellido", max_length=50, null=False)
    segundo_apellido = models.CharField("Segundo_apellido", max_length=50, null=False)
    tipo_identificacion = models.CharField("Tipo_identificación", max_length=50, choices=tipo_identificacion_opciones, null=False, help_text="Tipo de documento del cliente")
    numero_identificacion = models.BigIntegerField(
        'Numero_identificacion', unique=True, null=False, help_text="Agregar el numero de identificacion del cliente sin puntos"
    )
    direccion = models.CharField(
        'Direccion', max_length=255, null=False, help_text="Dirección donde se encuentra el cliente"
    )
    ciudad_residencia = models.CharField(
        'Ciudad_residencia', max_length=255, null=False, help_text="Ciudad donde se encuentra el cliente"
    )
    numero_celular = models.BigIntegerField(
        'Telefono',unique=True, null=False,help_text="Numero de contacto del cliente"
    )
    correo = models.EmailField(
        "Correo_electronico", max_length=254, null=False, unique=True, help_text="Correo electronico de contacto del cliente"
    )
    
    class Meta:
        db_table = "cliente"
        verbose_name_plural = "Clientes"
        db_table_comment = "Tabla con informacion de los clientes"
        ordering = ["primer_nombre",]
        
    def __str__(self):
        return f"{self.primer_nombre} {self.segundo_nombre} {self.primer_apellido} {self.segundo_apellido}"
    

class Orden(models.Model):
    fecha_creacion_orden = models.DateTimeField(
        'Fecha_creación_orden', auto_now_add=True
    )
    cliente = models.ForeignKey(Cliente, related_name="cliente_orden",on_delete=models.CASCADE
    )
    direccion_entrega = models.CharField(
        'Direccion_entrega', max_length=255, null=False, help_text="Dirección donde se entrega la orden"
    )
    orden_producto = models.ManyToManyField(
        Producto, related_name="orden_producto", through="OrdenProducto"
    )
    total = models.DecimalField("total_orden", decimal_places=2, max_digits=30, null=False, help_text="Precio Total de la orden")
    

    class Meta:
        db_table = "orden"
        verbose_name_plural = "Ordenes"
        db_table_comment = "Tabla con informacion de las ordenes"
        ordering = ["fecha_creacion_orden",]

        
    def __str__(self):
        return "Numero orden: " + str(self.id)
    

class OrdenProducto(models.Model):
    id = models.AutoField(primary_key=True)
    producto_sku = models.ForeignKey(Producto, on_delete=models.CASCADE)
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField("Cantidad", null=False)
    precio_unitario = models.DecimalField("Precio_unitario", decimal_places=2, max_digits=15)

    class Meta:
        db_table = "orden_producto"
        verbose_name_plural = "Ordenes_productos"
        db_table_comment = "Tabla con informacion de detallada de la orden"
        ordering = ["id",]


    def __str__(self):
        return "Numero detalle: " + str(self.id) + "con la orden" + str(self.orden)


class Seguimiento(models.Model):
    estado = models.PositiveIntegerField("Estado", null=False)
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    fecha_actualizacion_estado = models.DateTimeField('fecha_actualizacion_estado',auto_now=True)
    
    class Meta:
        db_table = "seguimiento"
        verbose_name_plural = "Seguimientos"
        db_table_comment = "Tabla con el seguimiento de los productos"
        ordering = ["-id",]


    def __str__(self):
        return f"Estado de la orden: {self.estado}"


class IngresoProducto(models.Model):
    producto = models.ForeignKey(
        Producto, related_name="ingresos_producto", on_delete=models.CASCADE
    )
    cantidad = models.PositiveIntegerField("Cantidad", null=False)
    fecha_ingreso = models.DateTimeField(
        'Fecha_ingreso', auto_now=True
    )
    
    class Meta:
        db_table = "ingreso_producto"
        verbose_name_plural = "Ingreso_productos"
        db_table_comment = "Tabla con los ingresos de productos al stock"
        ordering = ["id",]
        triggers = [
            pgtrigger.Trigger(
            name="actualizar_stock_ingresos_insert",
            when=pgtrigger.After,
            operation=pgtrigger.Insert,
            func=pgtrigger.Func(
                """
                    BEGIN
                        UPDATE producto
                        SET stock_actual = stock_actual + NEW.cantidad
                        WHERE sku = NEW.producto_id;
                        RETURN NEW;
                    END;
                """
            )
        )
        ,pgtrigger.Trigger(
            name="actualizar_stock_ingresos_update",
            when=pgtrigger.After,
            operation=pgtrigger.Update,
            func=pgtrigger.Func(
                """
                BEGIN
                        UPDATE producto
                        SET stock_actual = stock_actual + 
                            CASE
                                WHEN NEW.cantidad > OLD.cantidad THEN NEW.cantidad - OLD.cantidad
                                WHEN NEW.cantidad < OLD.cantidad THEN NEW.cantidad - OLD.cantidad
                                ELSE 0
                            END
                        WHERE sku = NEW.producto_id;
                        RETURN NEW;
                    END;
                """
            )
        )]
        

    def __str__(self):
        return f"fecha de ingreso: {self.fecha_ingreso}"


class SalidaProducto(models.Model):
    producto = models.ForeignKey(
        Producto, related_name="salidas_producto", on_delete=models.CASCADE
    )
    cantidad = models.PositiveIntegerField("Cantidad", null=False)
    fecha_salida = models.DateTimeField(
        'Fecha_salida', auto_now=True
    )
    orden = models.ForeignKey(
        Orden, related_name="salidas_producto", on_delete=models.CASCADE
    )
    
    class Meta:
        db_table = "salida_producto"
        verbose_name_plural = "Salida_productos"
        db_table_comment = "Tabla con los productos que salieron del stock"
        ordering = ["id",]
        triggers = [
            pgtrigger.Trigger(
            name="actualizar_stock_salida_insert",
            when=pgtrigger.After,
            operation=pgtrigger.Insert,
            func=pgtrigger.Func(
                """
                    BEGIN
                        UPDATE producto
                        SET stock_actual = stock_actual - NEW.cantidad
                        WHERE sku = NEW.producto_id;
                        RETURN NEW;
                    END;
                """
            )
        )
        ,pgtrigger.Trigger(
            name="actualizar_stock_ingresos_update",
            when=pgtrigger.After,
            operation=pgtrigger.Update,
            func=pgtrigger.Func(
                """
                BEGIN
                        UPDATE producto
                        SET stock_actual = 
                            CASE
                                WHEN NEW.cantidad > OLD.cantidad THEN stock_actual - (NEW.cantidad - OLD.cantidad)
                                WHEN NEW.cantidad < OLD.cantidad THEN stock_actual + (OLD.cantidad - NEW.cantidad)
                                ELSE 0
                            END
                        WHERE sku = NEW.producto_id;
                        RETURN NEW;
                    END;
                """
            )
        )]

    def __str__(self):
        return f"fecha de salida: {self.fecha_salida}"


class DevolucionProducto(models.Model):
    producto = models.ForeignKey(
        Producto, related_name="devoluciones_producto", on_delete=models.CASCADE
    )
    cantidad = models.PositiveIntegerField("Cantidad", null=False)
    fecha_devolucion = models.DateTimeField(
        'Fecha_devolucion', auto_now=True
    )
    orden = models.ForeignKey(
        Orden, related_name="devoluciones_producto", on_delete=models.CASCADE
    )
    motivo_devolucion = models.CharField(
        'motivo_devolucion', max_length=255, null=False, help_text="Motivo por el cual se realiza la devolución"
    )
    
    class Meta:
        db_table = "devolucion_producto"
        verbose_name_plural = "Devoluciones_productos"
        db_table_comment = "Tabla con los productos devueltos"
        ordering = ["id",]

    def __str__(self):
        return f"fecha de devolución: {self.fecha_devolucion}"

