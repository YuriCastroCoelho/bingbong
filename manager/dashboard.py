from django.db.models import Count, DecimalField, ExpressionWrapper, F, Q, Sum
from django.db.models.functions import TruncMonth

from .models import Item, Pedido, Produto

VALOR = ExpressionWrapper(F('quantidade') * F('preco'),
                          output_field=DecimalField(max_digits=12, decimal_places=2))
STATUS = dict(Pedido.STATUS_CHOICES)


def itens_do_vendedor(v):
    return Item.objects.filter(produto__vendedor=v)


def kpis(itens):
    vendas = itens.exclude(pedido__status='carrinho')
    d = vendas.aggregate(
        faturamento=Sum(VALOR),
        unidades=Sum('quantidade'),
        pedidos=Count('pedido', distinct=True),
        com_cupom=Count('pedido', distinct=True, filter=Q(pedido__cupom__isnull=False)),
    )
    d['faturamento'] = d['faturamento'] or 0
    d['unidades'] = d['unidades'] or 0
    d['ticket_medio'] = d['faturamento'] / d['pedidos'] if d['pedidos'] else 0
    return d


def ranking_produtos(itens, n=5):
    return (itens.exclude(pedido__status='carrinho')
            .values('produto__nome')
            .annotate(qtd=Sum('quantidade'), receita=Sum(VALOR))
            .order_by('-qtd')[:n])


def vendas_por_mes(itens):
    qs = (itens.exclude(pedido__status='carrinho')
          .annotate(mes=TruncMonth('pedido__data_hora'))
          .values('mes')
          .annotate(total=Sum(VALOR), pedidos=Count('pedido', distinct=True))
          .order_by('mes'))
    return [{'mes': r['mes'].strftime('%m/%Y'),
             'total': float(r['total'] or 0),
             'pedidos': r['pedidos']} for r in qs]


def por_status(itens):
    qs = (itens.values('pedido__status')
          .annotate(pedidos=Count('pedido', distinct=True))
          .order_by('pedido__status'))
    return [{'status': STATUS.get(r['pedido__status'], r['pedido__status']),
             'pedidos': r['pedidos']} for r in qs]


def estoque_baixo(v, limite=5):
    return Produto.objects.filter(vendedor=v, estoque__lte=limite).order_by('estoque')