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
    
class Pedido(models.Model):
    STATUS_CHOICES = [
        ('carrinho', 'No Carrinho'),
        ('pendente', 'Pagamento Pendente'),
        ('caminho', 'A caminho'),
        ('entregue', 'Produto Entregue')
    ]
    nome_cliente = models.CharField(max_length=100)
    data_hora = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='carrinho')
    
    def __str__(self):
        return f"Pedido {self.id} - {self.nome_cliente}"
    
class Item(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantidade} x {self.produto.nome} (Pedido {self.pedido.id})"
    