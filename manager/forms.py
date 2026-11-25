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


class ProdutoPainelForm(ProdutoForm):


    class Meta(ProdutoForm.Meta):
        fields = ['nome', 'estoque', 'preco', 'categoria']



class PeriodoForm(forms.Form):
    inicio = forms.DateField(required=False)
    fim = forms.DateField(required=False)


def filtrar_periodo(request, qs):
  
    form = PeriodoForm(request.GET)
    if form.is_valid():
        if form.cleaned_data['inicio']:
            qs = qs.filter(pedido__data_hora__date__gte=form.cleaned_data['inicio'])
        if form.cleaned_data['fim']:
            qs = qs.filter(pedido__data_hora__date__lte=form.cleaned_data['fim'])
    return qs