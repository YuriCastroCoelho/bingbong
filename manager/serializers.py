from rest_framework import serializers
from .models import Item, Pedido, Produto


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['id', 'nome', 'preco', 'estoque', 'categoria'] 

    def validate_preco(self, value):
        if value <= 0:
            raise serializers.ValidationError('O preço deve ser maior que zero.')
        return value

    def validate_nome(self, value):
        v = self.context['request'].user.perfil.vendedor
        qs = Produto.objects.filter(vendedor=v, nome=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('Você já tem um produto com este nome.')
        return value


class ItemSerializer(serializers.ModelSerializer):
    produto = serializers.StringRelatedField()

    class Meta:
        model = Item
        fields = ['id', 'produto', 'quantidade', 'preco']


class PedidoSerializer(serializers.ModelSerializer):
    cliente = serializers.StringRelatedField()
    cupom = serializers.StringRelatedField()
    itens = ItemSerializer(source='itens_vendedor', many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = ['id', 'cliente', 'data_hora', 'status', 'cupom', 'itens']