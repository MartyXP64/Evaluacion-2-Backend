from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Videojuego

# 1. Vista del catálogo principal (protegida completa)
@login_required
def catalogo(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        categoria = request.POST.get('categoria')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        portada = request.POST.get('portada')
        descripcion = request.POST.get('descripcion')

        if not portada:
            portada = 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=500'

        Videojuego.objects.create(
            titulo=titulo,
            categoria=categoria,
            precio=precio,
            stock=stock,
            portada=portada,
            descripcion=descripcion
        )
        return redirect('catalogo')

    juegos = Videojuego.objects.all()
    return render(request, 'index.html', {'juegos': juegos})

# 2. Vista para eliminar (recuperada y protegida)
@login_required
def eliminar_videojuego(request, id):
    juego = get_object_or_404(Videojuego, id=id)
    juego.delete()
    return redirect('catalogo') 

# 3. Vista para editar (recuperada y protegida)
@login_required
def editar_videojuego(request, id):
    juego = get_object_or_404(Videojuego, id=id)

    if request.method == 'POST':
        juego.titulo = request.POST.get('titulo')
        juego.categoria = request.POST.get('categoria')
        juego.precio = request.POST.get('precio')
        juego.stock = request.POST.get('stock')
        juego.portada = request.POST.get('portada')
        juego.descripcion = request.POST.get('descripcion')
        
        juego.save() 
        
    return redirect('catalogo')