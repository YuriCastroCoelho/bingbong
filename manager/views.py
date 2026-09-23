from django.shortcuts import render, redirect
from .models import Produto , Cliente, Pedido, Item

# Create your views here.
def lista_produtos(request):
    
    produtos = Produto.objects.all()
    
    
    return render(
        request, 
        'manager/lista_produtos.html',  
        {'produtos': produtos}       
    )

def adicionar_ao_carrinho(request, produto_id):

    if request.method == 'POST':

        produto = Produto.objects.get(id=produto_id)

        valor_do_campo = request.POST.get('cliente_username')

        cliente, foi_criado = Cliente.objects.get_or_create(nome=valor_do_campo)
        
        pedido, foi_criado_pedido = Pedido.objects.get_or_create(
            cliente = cliente,
            status = 'carrinho'
        )

        quantidade = request.POST.get('quantidade')
        
        Item.objects.create(
            pedido = pedido,
            produto = produto,
            quantidade = quantidade,
            preco = produto.preco
        )
        
        return redirect('lista_produtos')
    
def ver_carrinho(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    itens = Item.objects.filter(pedido=pedido)
    
    total = 0
    for item in itens:
        total = total + (item.quantidade * item.preco)
    
    return render(
        request,
        'manager/ver_carrinho.html',
        {'pedido': pedido, 'itens': itens, 'total': total},
    )
    
