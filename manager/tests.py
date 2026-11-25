from django.test import TestCase

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Cliente, Item, Pedido, Perfil, Produto, Vendedor


class IsolamentoTest(TestCase):
    def setUp(self):
        self.va = Vendedor.objects.create(marca='A', contato='a@a.com')
        self.vb = Vendedor.objects.create(marca='B', contato='b@b.com')
        self.ua = User.objects.create_user('ana', password='x')
        Perfil.objects.create(usuario=self.ua, vendedor=self.va, papel='admin')
        self.pa = Produto.objects.create(nome='Mouse', preco=10, estoque=5,
                                         categoria='x', vendedor=self.va)
        self.pb = Produto.objects.create(nome='Fone', preco=20, estoque=5,
                                         categoria='x', vendedor=self.vb)
        cli = Cliente.objects.create(nome='João')
        for _ in range(3):                       # 3 pedidos do vendedor A
            p = Pedido.objects.create(cliente=cli, status='pendente')
            Item.objects.create(pedido=p, produto=self.pa, quantidade=1, preco=10)
        for _ in range(5):                       # 5 pedidos do vendedor B
            p = Pedido.objects.create(cliente=cli, status='pendente')
            Item.objects.create(pedido=p, produto=self.pb, quantidade=1, preco=20)
        self.client.force_login(self.ua)

    def test_dashboard_so_do_vendedor(self):
        r = self.client.get('/painel/dashboard/')
        self.assertEqual(r.context['kpis']['pedidos'], 3)
        self.assertEqual(r.context['kpis']['faturamento'], 30)

    def test_dashboard_sem_dados_nao_quebra(self):
        Pedido.objects.all().delete()
        self.assertEqual(self.client.get('/painel/dashboard/').status_code, 200)

    def test_data_invalida_nao_gera_500(self):
        self.assertEqual(self.client.get('/painel/dashboard/?inicio=abc').status_code, 200)

    def test_editar_produto_de_outro_vendedor_da_404(self):
        r = self.client.get(f'/painel/produtos/{self.pb.id}/editar/')
        self.assertEqual(r.status_code, 404)

    def test_api_nao_mostra_produto_de_outro(self):
        self.assertEqual(self.client.get(f'/api/produtos/{self.pb.id}/').status_code, 404)
        nomes = [p['nome'] for p in self.client.get('/api/produtos/').json()]
        self.assertEqual(nomes, ['Mouse'])