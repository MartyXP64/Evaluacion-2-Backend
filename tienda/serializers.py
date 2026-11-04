from rest_framework import serializers
from .models import Videojuego

class VideojuegoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videojuego
        fields = '__all__' # Esto convierte todos los campos de tu tabla a JSON


        