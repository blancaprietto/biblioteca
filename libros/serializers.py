from rest_framework import serializers
from .models import Libro, Autor, Genero, Calificacion

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'

class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = '__all__'

class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = '__all__'

class CalificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calificacion
        fields = ['id', 'libro', 'puntaje']  # NO incluimos 'usuario'

    def validate_puntaje(self, value):
        if not 1.0 <= value <= 5.0:
            raise serializers.ValidationError("El puntaje debe estar entre 1.0 y 5.0.")
        return value