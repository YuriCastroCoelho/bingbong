from django.urls import path
from . import api_views

urlpatterns = [
    path('produtos/', api_views.ProdutoListCreate.as_view()),
    path('produtos/<int:pk>/', api_views.ProdutoDetail.as_view()),
    path('pedidos/', api_views.PedidoList.as_view()),
    path('pedidos/<int:pk>/', api_views.PedidoDetail.as_view()),
    path('dashboard/', api_views.DashboardApi.as_view()),
]