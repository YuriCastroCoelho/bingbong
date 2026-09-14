from django.db import models

# Create your models here.
class Vendedor(models.Model):
    marca = models.CharField(max_length=100)
    contato = models.EmailField(max_length=200)
    
    def __str__(self):
        return self.marca
    
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()
    categoria = models.CharField(max_length=100)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nome    