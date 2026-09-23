from django.shortcuts import render, redirect
from .models import Produto , Cliente, Pedido, Item, Cupom
from datetime import date
from django.contrib import messages

# Create your views here.
def lista_produtos(request):
    
    produtos = Produto.objects.all()
    
    
    return render(
        request, 
        'manager/lista_produtos.html',  
        {'produtos': produtos}       
    )
    
def ver_carrinho(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    itens = Item.objects.filter(pedido=pedido)
    
    total = 0
    for item in itens:
        total = total + (item.quantidade * item.preco)
    if pedido.cupom and pedido.cupom.validade >= date.today():
        total = total - pedido.cupom.desconto

    cupom_valido = Cupom.objects.filter(utilizado=False, validade__gte=date.today())

    return render(
        request,
        'manager/ver_carrinho.html',
        {'pedido': pedido, 'itens': itens, 'total': total, 'cupons': cupom_valido},
    )
    
def adicionar_ao_carrinho(request, produto_id):
    if request.method == 'POST':
        produto = Produto.objects.get(id=produto_id)

        valor_do_campo = request.POST.get('cliente_username')
        cliente, foi_criado = Cliente.objects.get_or_create(nome=valor_do_campo)

        pedido, foi_criado_pedido = Pedido.objects.get_or_create(
            cliente=cliente,
            status='carrinho'
        )

        quantidade = int(request.POST.get('quantidade'))

        Item.objects.create(
            pedido=pedido,
            produto=produto,
            quantidade=quantidade,
            preco=produto.preco
        )

        produto.estoque = produto.estoque - quantidade
        produto.save()

        return redirect('ver_carrinho', pedido_id = pedido.id)

def aplicar_cupom(request, pedido_id):
    if request.method == 'POST':
        pedido = Pedido.objects.get(id=pedido_id)
        codigo_cupom = request.POST.get('codigo_cupom')

        try:
            cupom = Cupom.objects.get(codigo=codigo_cupom)
            pedido.cupom = cupom
            pedido.save()
            messages.success(request, f'Cupom "{cupom.codigo}" aplicado!')
        except Cupom.DoesNotExist:
            messages.error(request, 'Cupom inválido.')

        return redirect('ver_carrinho', pedido_id=pedido.id)
    
def finalizar_pedido(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    pedido.status = 'pendente'
    pedido.save()
    return redirect('ver_carrinho', pedido_id=pedido.id)


def marcar_a_caminho(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    pedido.status = 'caminho'
    pedido.save()
    return redirect('ver_carrinho', pedido_id=pedido.id)


def marcar_entregue(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    pedido.status = 'entregue'
    pedido.save()
    pedido.delete()
    return redirect('lista_produtos')


def cancelar_pedido(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    itens = Item.objects.filter(pedido=pedido)

    for item in itens:
        produto = item.produto
        produto.estoque = produto.estoque + item.quantidade
        produto.save()

    pedido.delete()
    return redirect('lista_produtos')