def vendedor_atual(request):
  
    return request.user.perfil.vendedor