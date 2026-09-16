from django.shortcuts import render
from .models import Produto  

# Create your views here.
def lista_produtos(request):
    
    produtos = Produto.objects.all()
    
    
    return render(
        request, 
        'manager/lista_produtos.html',  
        {'produtos': produtos}       
    )