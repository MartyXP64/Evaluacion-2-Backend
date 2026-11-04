from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Videojuego
from django.contrib import messages
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import VideojuegoSerializer

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


        if not request.user.is_superuser:
            return redirect('catalogo')
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
    if not request.user.is_superuser:
        return redirect('catalogo')
    juego = get_object_or_404(Videojuego, id=id)
    juego.delete()
    return redirect('catalogo') 

# 3. Vista para editar (recuperada y protegida)
@login_required
def editar_videojuego(request, id):
    if not request.user.is_superuser:
        return redirect('catalogo')
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

def comprar_juego(request, id):
    
    if request.user.is_superuser:
        messages.warning(request, "Los administradores no pueden comprar juegos.")
        return redirect('catalogo')

    juego = Videojuego.objects.get(id=id)

    
    if juego.stock > 0:
        juego.stock -= 1  
        juego.save()      
        messages.success(request, f"¡Compraste '{juego.titulo}' con éxito!")
    else:
        messages.error(request, f"Lo sentimos, '{juego.titulo}' está agotado.")

    return redirect('catalogo')

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated]) 
def api_juegos(request):
    if request.method == 'GET':
        juegos = Videojuego.objects.all()
        serializer = VideojuegoSerializer(juegos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = VideojuegoSerializer(data=request.data)
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated]) 
def api_juego_detalle(request, id):
   
    try:
        juego = Videojuego.objects.get(id=id)
    except Videojuego.DoesNotExist:
        return Response({'error': 'Videojuego no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VideojuegoSerializer(juego)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = VideojuegoSerializer(juego, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        juego.delete()
        return Response({'mensaje': 'Juego eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)