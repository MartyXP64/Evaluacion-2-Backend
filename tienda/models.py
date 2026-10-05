from django.db import models

class Videojuego(models.Model):
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.CharField(max_length=50)
    precio = models.IntegerField()
    stock = models.IntegerField(default=1)
    portada = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.titulo
