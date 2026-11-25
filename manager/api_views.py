from django.db.models import Prefetch
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from . import dashboard as dash
from .forms import filtrar_periodo
from .models import Item, Pedido, Produto
from .serializers import PedidoSerializer, ProdutoSerializer


class DoVendedorMixin:
    def get_queryset(self):
        v = self.request.user.perfil.vendedor
        return super().get_queryset().filter(vendedor=v)

    def perform_create(self, serializer):
        serializer.save(vendedor=self.request.user.perfil.vendedor)


class ProdutoListCreate(DoVendedorMixin, generics.ListCreateAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer


class ProdutoDetail(DoVendedorMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer


class PedidosDoVendedor:
    serializer_class = PedidoSerializer

    def get_queryset(self):
        v = self.request.user.perfil.vendedor
        meus_itens = Item.objects.filter(produto__vendedor=v).select_related('produto')
        return (Pedido.objects.filter(item__produto__vendedor=v)
                .exclude(status='carrinho').distinct()
                .select_related('cliente', 'cupom')
                .prefetch_related(Prefetch('item_set', queryset=meus_itens,
                                           to_attr='itens_vendedor'))
                .order_by('-data_hora'))


class PedidoList(PedidosDoVendedor, generics.ListAPIView):
    pass


class PedidoDetail(PedidosDoVendedor, generics.RetrieveAPIView):
    pass


class DashboardApi(APIView):
    def get(self, request):
        v = request.user.perfil.vendedor
        itens = filtrar_periodo(request, dash.itens_do_vendedor(v))
        return Response({
            'kpis': dash.kpis(itens),
            'ranking': list(dash.ranking_produtos(itens)),
            'por_mes': dash.vendas_por_mes(itens),
            'por_status': dash.por_status(itens),
        })