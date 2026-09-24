from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'estoque', 'preco', 'categoria', 'vendedor']
    
    def clean_preco(self):
        valor = self.cleaned_data.get('preco')
        if valor <= 0:
            raise forms.ValidationError("Preço Invalido. Tem que ser maior que 0")
        return valor

    
    def clean_estoque(self):
        valor = self.cleaned_data.get('estoque')
        if valor <= 0:
            raise forms.ValidationError("Estoque Invalido Não pode ser negativo")
        return valor
    

