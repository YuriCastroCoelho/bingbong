from django.contrib import admin

# Register your models here.
from .models import Cliente, Vendedor, Produto, Pedido, Item, Cupom, Perfil

admin.site.register(Cliente)
admin.site.register(Vendedor)
admin.site.register(Pedido)
admin.site.register(Item)
admin.site.register(Cupom)
admin.site.register(Perfil)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'vendedor', 'preco', 'estoque')
    list_filter = ('vendedor',)