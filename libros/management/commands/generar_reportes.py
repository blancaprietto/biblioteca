from django.core.management.base import BaseCommand
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import subprocess
from libros.models import Autor, Genero, Libro, Calificacion
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Genera 10 gráficos de análisis de libros y calificaciones'

    def handle(self, *args, **kwargs):
        sns.set(style="whitegrid")

        # Crear carpeta de salida
        output_dir = os.path.join(os.getcwd(), 'reportes_png')
        os.makedirs(output_dir, exist_ok=True)

        # Cargar datos
        df_libros = pd.DataFrame(list(Libro.objects.all().values()))
        df_autores = pd.DataFrame(list(Autor.objects.all().values()))
        df_generos = pd.DataFrame(list(Genero.objects.all().values()))
        df_users = pd.DataFrame(list(User.objects.all().values('id', 'username')))
        df_calificaciones = pd.DataFrame(list(Calificacion.objects.all().values()))

        if df_calificaciones.empty or df_libros.empty:
            self.stdout.write(self.style.WARNING("⚠️ No hay datos suficientes para generar los reportes."))
            return

        # Unificar datos
        df = df_calificaciones.merge(df_libros, left_on='libro_id', right_on='id', suffixes=('_cal', '_libro'))
        df = df.merge(df_users, left_on='usuario_id', right_on='id', suffixes=('', '_user'))
        df = df.merge(df_autores, left_on='autor_id', right_on='id', suffixes=('', '_autor'))
        df = df.merge(df_generos, left_on='genero_id', right_on='id', suffixes=('', '_genero'))

        # 1. Distribución general de puntajes
        plt.figure()
        sns.histplot(df['puntaje'], bins=10, kde=True)
        plt.title("Distribución general de puntajes")
        plt.savefig(os.path.join(output_dir, "reporte1_puntajes.png"))

        # 2. Top 10 libros mejor calificados
        plt.figure()
        top_libros = df.groupby('titulo')['puntaje'].mean().sort_values(ascending=False).head(10)
        top_libros.plot(kind='barh')
        plt.title("Top 10 libros mejor calificados")
        plt.xlabel("Puntaje promedio")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "reporte2_libros_top.png"))

        # 3. Promedio de calificación por género
        plt.figure()
        sns.barplot(data=df, x='nombre_genero', y='puntaje', estimator='mean', errorbar=None)
        plt.title("Puntaje promedio por género")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "reporte3_genero_promedio.png"))

        # 4. Autores con más libros
        plt.figure()
        libros_por_autor = df_autores.merge(df_libros, left_on='id', right_on='autor_id')
        libros_por_autor.groupby('nombre')['id_y'].count().sort_values(ascending=False).head(10).plot(kind='barh')
        plt.title("Autores con más libros")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "reporte4_autores_mas_libros.png"))

        # 5. Libros con más calificaciones (barra horizontal legible)
        plt.figure(figsize=(10, 6))
        libros_mas_calificados = df.groupby('titulo')['puntaje'].count().sort_values(ascending=True).tail(10)
        libros_mas_calificados.plot(kind='barh', color='steelblue')
        plt.title("Libros con más calificaciones")
        plt.xlabel("Cantidad de calificaciones")
        plt.ylabel("Título del libro")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "reporte5_libros_mas_calificaciones.png"))


        # 6. Usuarios que más califican
        plt.figure()
        df.groupby('username')['puntaje'].count().sort_values(ascending=False).head(10).plot(kind='bar')
        plt.title("Usuarios que más califican")
        plt.ylabel("Cantidad")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "reporte6_usuarios_mas_califican.png"))

        # 7. Usuarios con puntaje promedio más alto
        plt.figure()
        df.groupby('username')['puntaje'].mean().sort_values(ascending=False).head(10).plot(kind='bar')
        plt.title("Usuarios más exigentes (prom. alto)")
        plt.ylabel("Promedio")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "reporte7_usuarios_promedio.png"))

        # 8. Puntaje promedio por año
        if 'fecha_lanzamiento' in df.columns:
            df['anio'] = pd.to_datetime(df['fecha_lanzamiento']).dt.year
            plt.figure()
            sns.lineplot(data=df, x='anio', y='puntaje', errorbar=None)
            plt.title("Puntaje promedio por año de publicación")
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, "reporte8_promedio_anio.png"))

        # 9. Distribución de calificaciones por género
        plt.figure()
        df['nombre_genero'].value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.title("Distribución de calificaciones por género")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "reporte9_calificaciones_genero.png"))

        # 10. Mapa de calor de correlaciones con variables numéricas
        plt.figure()

        # Crear variables numéricas auxiliares
        df['anio'] = pd.to_datetime(df['fecha_lanzamiento']).dt.year
        df_corr = df.groupby('libro_id').agg({
            'puntaje': ['mean', 'count'],
            'anio': 'first'
        })

        # Renombrar columnas para claridad
        df_corr.columns = ['promedio_puntaje', 'cantidad_calificaciones', 'anio']
        corr_matrix = df_corr.corr()

        # Plot
        sns.heatmap(corr_matrix, annot=True, cmap="YlGnBu", fmt=".2f")
        plt.title("Matriz de correlación entre variables numéricas")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "reporte10_heatmap.png"))

        self.stdout.write(self.style.SUCCESS("✅ 10 reportes generados en la carpeta 'reportes_png'."))
