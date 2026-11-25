from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProdutoForm
from .models import Item, Pedido, Produto
from .utils import vendedor_atual


@login_required
def painel_produtos(request):
    v = vendedor_atual(request)
    produtos = Produto.objects.filter(vendedor=v)              # SEMPRE filtra
    return render(request, 'manager/painel_produtos.html', {'produtos': produtos})


@login_required
def painel_novo_produto(request):
    v = vendedor_atual(request)
    form = ProdutoForm(request.POST or None)
    if form.is_valid():
        produto = form.save(commit=False)
        produto.vendedor = v                                    # vem do usuário
        produto.save()
        return redirect('painel_produtos')
    return render(request, 'manager/painel_form.html', {'form': form})


@login_required
def painel_editar_produto(request, produto_id):
    v = vendedor_atual(request)
    produto = get_object_or_404(Produto, pk=produto_id, vendedor=v)   # 404 se for de outro
    form = ProdutoForm(request.POST or None, instance=produto)
    if form.is_valid():
        form.save()
        return redirect('painel_produtos')
    return render(request, 'manager/painel_form.html', {'form': form})


@login_required
def painel_pedidos(request):
    v = vendedor_atual(request)
    itens = (Item.objects.filter(produto__vendedor=v)
             .exclude(pedido__status='carrinho')
             .select_related('pedido', 'pedido__cliente', 'produto')   # evita N+1
             .order_by('-pedido__data_hora'))
    return render(request, 'manager/painel_pedidos.html', {'itens': itens})


@login_required
def painel_pedido(request, pedido_id):
    v = vendedor_atual(request)
    # distinct() porque o JOIN com Item repete o pedido (um por item do vendedor)
    meus = Pedido.objects.filter(item__produto__vendedor=v).distinct()
    pedido = get_object_or_404(meus, pk=pedido_id)
    itens = pedido.item_set.filter(produto__vendedor=v).select_related('produto')
    return render(request, 'manager/painel_pedido.html',
                  {'pedido': pedido, 'itens': itens})