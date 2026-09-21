from django.urls import path
from . import views

urlpatterns = [
    path(
        'produtos/',                
        views.lista_produtos,       
        name='lista_produtos'      
    ),
    path(
        'produtos/<int:produto_id>/adicionar/',
        views.adicionar_ao_carrinho,
        name = 'adicionar_carrinho'
    )
]