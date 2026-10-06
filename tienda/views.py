from django.shortcuts import render, redirect, get_object_or_404
from .models import Videojuego

# --- VISTA PRINCIPAL (CREAR Y LEER) ---
def catalogo(request):
    if request.method == 'POST':
        # Rescatamos los datos enviados por el modal de "Añadir Nuevo"
        titulo = request.POST.get('titulo')
        categoria = request.POST.get('categoria')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        portada = request.POST.get('portada')
        descripcion = request.POST.get('descripcion')

        # Si no ponen imagen, usamos una por defecto
        if not portada:
            portada = 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=500'

        # Guardamos en la base de datos
        Videojuego.objects.create(
            titulo=titulo,
            categoria=categoria,
            precio=precio,
            stock=stock,
            portada=portada,
            descripcion=descripcion
        )
        return redirect('catalogo')

    # ESTO FALTABA: Si no es POST (o sea, solo entró a mirar la página)
    # Buscamos todos los juegos y los enviamos al index.html
    juegos = Videojuego.objects.all()
    return render(request, 'index.html', {'juegos': juegos})


# --- VISTA PARA ELIMINAR ---
def eliminar_videojuego(request, id):
    juego = get_object_or_404(Videojuego, id=id)
    juego.delete()
    return redirect('catalogo') 


# --- VISTA PARA EDITAR (CON MODAL) ---
def editar_videojuego(request, id):
    juego = get_object_or_404(Videojuego, id=id)

    # Solo procesamos si el modal de edición envía información (POST)
    if request.method == 'POST':
        juego.titulo = request.POST.get('titulo')
        juego.categoria = request.POST.get('categoria')
        juego.precio = request.POST.get('precio')
        juego.stock = request.POST.get('stock')
        juego.portada = request.POST.get('portada')
        juego.descripcion = request.POST.get('descripcion')
        
        juego.save() # Se actualiza en la base de datos
        
    return redirect('catalogo')