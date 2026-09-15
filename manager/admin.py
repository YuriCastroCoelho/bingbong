from django.contrib import admin

# Register your models here.
from .models import Cliente, Vendedor, Produto, Pedido, Item, Cupom

admin.site.register(Cliente)
admin.site.register(Vendedor)
admin.site.register(Produto)
admin.site.register(Pedido)
admin.site.register(Item)
admin.site.register(Cupom)