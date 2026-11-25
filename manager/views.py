from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.db.models import F
from .models import Produto, Cliente, Pedido, Item, Cupom
from datetime import date
from django.contrib import messages

# Create your views here.
def lista_produtos(request):
    
    produtos = Produto.objects.all()
    
    termo_achar = request.GET.get('q')
    categoria_filtro = request.GET.get('categoria')

    if termo_achar:
        produtos = produtos.filter(nome__icontains=termo_achar)

    if categoria_filtro:
        produtos = produtos.filter(categoria=categoria_filtro)
    
    
    return render(
        request,
        'manager/lista_produtos.html',
        {'produtos': produtos, 'termo_achar': termo_achar, 'categoria_filtro': categoria_filtro},
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
        produto = get_object_or_404(Produto, id=produto_id)

        try:
            quantidade = int(request.POST.get('quantidade'))
        except (TypeError, ValueError):
            quantidade = 0
        if quantidade <= 0:
            messages.error(request, 'Informe uma quantidade aceitável.')
            return redirect('lista_produtos')

        valor_do_campo = request.POST.get('cliente_username')
        cliente, foi_criado = Cliente.objects.get_or_create(nome=valor_do_campo)

        pedido, foi_criado_pedido = Pedido.objects.get_or_create(
            cliente=cliente,
            status='carrinho'
        )

        with transaction.atomic():
            baixou = Produto.objects.filter(
                pk=produto.pk, estoque__gte=quantidade
            ).update(estoque=F('estoque') - quantidade)

            if not baixou:
                messages.error(request, 'Estoque insuficiente.')
                return redirect('lista_produtos')

            Item.objects.create(
                pedido=pedido,
                produto=produto,
                quantidade=quantidade,
                preco=produto.preco
            )

        return redirect('ver_carrinho', pedido_id=pedido.id)

    return redirect('lista_produtos')
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

def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'manager/cadastro_produto.html', {"form" : form})