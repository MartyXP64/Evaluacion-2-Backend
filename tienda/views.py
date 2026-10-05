from django.shortcuts import render, redirect
from .models import Videojuego

def catalogo(request):
    if request.method == 'POST':
        # Rescatamos los datos enviados por el modal
        titulo = request.POST.get('titulo')
        categoria = request.POST.get('categoria')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        portada = request.POST.get('portada')
        descripcion = request.POST.get('descripcion')

        # Si no ponen imagen, usamos una por defecto
        if not portada:
            portada = 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=500'

        # Guardamos en MySQL
        Videojuego.objects.create(
            titulo=titulo,
            categoria=categoria,
            precio=precio,
            stock=stock,
            portada=portada,
            descripcion=descripcion
        )
        return redirect('catalogo')

    # Traemos todos los juegos para mostrarlos
    juegos = Videojuego.objects.all()
    return render(request, 'index.html', {'juegos': juegos})