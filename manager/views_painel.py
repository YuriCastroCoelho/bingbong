import csv

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from . import dashboard as dash
from .forms import PeriodoForm, ProdutoPainelForm, filtrar_periodo
from .models import Item, Pedido, Produto
from .utils import vendedor_atual


@login_required
def painel_produtos(request):
    v = vendedor_atual(request)
    produtos = Produto.objects.filter(vendedor=v)
    return render(request, 'manager/painel_produtos.html', {'produtos': produtos})


@login_required
def painel_novo_produto(request):
    v = vendedor_atual(request)
    form = ProdutoPainelForm(request.POST or None)
    if form.is_valid():
        produto = form.save(commit=False)
        produto.vendedor = v
        produto.save()
        return redirect('painel_produtos')
    return render(request, 'manager/painel_form.html', {'form': form})


@login_required
def painel_editar_produto(request, produto_id):
    v = vendedor_atual(request)
    produto = get_object_or_404(Produto, pk=produto_id, vendedor=v)
    form = ProdutoPainelForm(request.POST or None, instance=produto)
    if form.is_valid():
        form.save()
        return redirect('painel_produtos')
    return render(request, 'manager/painel_form.html', {'form': form})


@login_required
def painel_pedidos(request):
    v = vendedor_atual(request)
    itens = (Item.objects.filter(produto__vendedor=v)
             .exclude(pedido__status='carrinho')
             .select_related('pedido', 'pedido__cliente', 'produto')
             .order_by('-pedido__data_hora'))
    return render(request, 'manager/painel_pedidos.html', {'itens': itens})


@login_required
def painel_pedido(request, pedido_id):
    v = vendedor_atual(request)
    meus = Pedido.objects.filter(item__produto__vendedor=v).distinct()
    pedido = get_object_or_404(meus, pk=pedido_id)
    itens = pedido.item_set.filter(produto__vendedor=v).select_related('produto')
    return render(request, 'manager/painel_pedido.html',
                  {'pedido': pedido, 'itens': itens})


@login_required
def dashboard(request):
    v = vendedor_atual(request)
    itens = filtrar_periodo(request, dash.itens_do_vendedor(v))
    contexto = {
        'kpis': dash.kpis(itens),
        'ranking': dash.ranking_produtos(itens),
        'por_mes': dash.vendas_por_mes(itens),
        'por_status': dash.por_status(itens),
        'estoque_baixo': dash.estoque_baixo(v),
        'form': PeriodoForm(request.GET),
        'mostra_series': request.user.perfil.eh_admin,
    }
    return render(request, 'manager/dashboard.html', contexto)


def _seguro(valor):
    texto = str(valor)
    return "'" + texto if texto[:1] in ('=', '+', '-', '@') else texto


@login_required
def exportar_csv(request):
    if not request.user.perfil.eh_admin:
        return HttpResponse(status=403)
    v = vendedor_atual(request)
    itens = (filtrar_periodo(request, dash.itens_do_vendedor(v))
             .exclude(pedido__status='carrinho')
             .select_related('pedido', 'pedido__cliente', 'produto')
             .order_by('pedido__data_hora'))
    resp = HttpResponse(content_type='text/csv')
    resp['Content-Disposition'] = 'attachment; filename="vendas.csv"'
    w = csv.writer(resp)
    w.writerow(['Pedido', 'Cliente', 'Produto', 'Qtd', 'Preço', 'Data', 'Status'])
    for i in itens:
        w.writerow([i.pedido_id, _seguro(i.pedido.cliente.nome), _seguro(i.produto.nome),
                    i.quantidade, i.preco, i.pedido.data_hora.date(),
                    i.pedido.get_status_display()])
    return resp