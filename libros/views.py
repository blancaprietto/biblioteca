from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Libro, Autor, Genero, Calificacion
from .serializers import LibroSerializer, AutorSerializer, GeneroSerializer, CalificacionSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError

#View para Autor
class AutorListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        autor = Autor.objects.all()
        serializer = AutorSerializer(autor, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AutorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AutorDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        autor = get_object_or_404(Autor, pk=pk)
        serializer = AutorSerializer(autor)
        return Response(serializer.data)

    def put(self, request, pk):
        permission_classes = [IsAuthenticated]
        autor = get_object_or_404(Autor, pk=pk)
        serializer = AutorSerializer(autor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        permission_classes = [IsAuthenticated]
        autor = get_object_or_404(Autor, pk=pk)
        autor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#View para genero
class GeneroListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        genero = Genero.objects.all()
        serializer = GeneroSerializer(genero, many=True)
        return Response(serializer.data)

    def post(self, request):
        permission_classes = [IsAuthenticated]
        serializer = GeneroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GeneroDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        genero = get_object_or_404(Genero, pk=pk)
        serializer = GeneroSerializer(genero)
        return Response(serializer.data)

    def put(self, request, pk):
        genero = get_object_or_404(Genero, pk=pk)
        serializer = GeneroSerializer(genero, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        genero = get_object_or_404(Genero, pk=pk)
        genero.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#View para Libro
class LibroListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        libros = Libro.objects.all()
        serializer = LibroSerializer(libros, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LibroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LibroDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        serializer = LibroSerializer(libro)
        return Response(serializer.data)

    def put(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        serializer = LibroSerializer(libro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        libro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#View para Calificaciones
class CalificacionListCreateView(APIView):
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados

    def get(self, request):
        calificaciones = Calificacion.objects.all()
        serializer = CalificacionSerializer(calificaciones, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CalificacionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(usuario=request.user)  # Forzamos que use el usuario autenticado
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'error': 'Ya calificaste este libro.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CalificacionDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        calificacion = get_object_or_404(Calificacion, pk=pk)
        serializer = CalificacionSerializer(calificacion)
        return Response(serializer.data)

    def put(self, request, pk):
        calificacion = get_object_or_404(Calificacion, pk=pk)
        serializer = CalificacionSerializer(calificacion, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        calificacion = get_object_or_404(Calificacion, pk=pk)
        calificacion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
