from django.db import models

# Create your models here.

class Comentarios(models.Model):
    nombre = models.CharField(max_length=50)
    email = models.EmailField()
    comentario = models.TextField(max_length=200)
    
    def __str__(self):
        return self.nombre
