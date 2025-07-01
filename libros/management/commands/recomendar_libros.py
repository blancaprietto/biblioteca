from django.core.management.base import BaseCommand
from libros.models import Libro, Genero
from django.db.models import Avg

class Command(BaseCommand):
    help = "Muestra en consola los libros mejor valorados por género"

    def add_arguments(self, parser):
        parser.add_argument('genero_id', type=int, help='ID del género a filtrar')

    def handle(self, *args, **kwargs):
        genero_id = kwargs['genero_id']

        # Obtener el nombre del género
        try:
            genero = Genero.objects.get(id=genero_id)
        except Genero.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"❌ El género con ID {genero_id} no existe."))
            return

        libros = Libro.objects.filter(genero_id=genero_id)\
            .annotate(promedio=Avg('calificaciones__puntaje'))\
            .order_by('-promedio')[:10]

        if not libros:
            self.stdout.write(self.style.WARNING(f"⚠️  No se encontraron libros para el género '{genero.nombre}'."))
            return

        self.stdout.write(self.style.SUCCESS(f"\n📚 Libros mejor valorados del género '{genero.nombre}':\n"))
        self.stdout.write(f"{'Título':40} {'Promedio':>8}")
        self.stdout.write(f"{'-'*48}")
        for libro in libros:
            promedio = round(libro.promedio or 0, 2)
            self.stdout.write(f"{libro.titulo:40} {promedio:>8}")
