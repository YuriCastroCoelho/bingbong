from django.shortcuts import render
from .models import Produto , Cliente

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

