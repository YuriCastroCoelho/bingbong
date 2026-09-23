from django.urls import path
from . import views

urlpatterns = [
    path(
        '',                
        views.lista_produtos,       
        name='lista_produtos'      
    ),
    path(
        'produtos/<int:produto_id>/adicionar/',
        views.adicionar_ao_carrinho,
        name = 'adicionar_carrinho'
    ),
    path(
        'carrinho/<int:pedido_id>/', 
        views.ver_carrinho, 
        name='ver_carrinho',
    ),
    path(
        'carrinho/<int:pedido_id>/aplicar-cupom/',
        views.aplicar_cupom, 
        name='aplicar_cupom'
    ),
    path(
        'carrinho/<int:pedido_id>/finalizar/',
        views.finalizar_pedido,
        name='finalizar_pedido'
    ),
    path(
        'carrinho/<int:pedido_id>/a-caminho/',
        views.marcar_a_caminho,
        name='marcar_a_caminho'
    ),
    path(
        'carrinho/<int:pedido_id>/entregue/',
        views.marcar_entregue,
        name='marcar_entregue'
    ),
    path(
        'carrinho/<int:pedido_id>/cancelar/',
        views.cancelar_pedido,
        name='cancelar_pedido'
    ),
]