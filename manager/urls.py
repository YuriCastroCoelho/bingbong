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
    )
]