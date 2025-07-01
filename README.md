# Biblioteca - Proyecto Django + PostgreSQL

Este proyecto es una API RESTful desarrollada en Django, que permite la gestión de libros, autores, géneros y calificaciones de usuarios. Incluye funcionalidades de análisis de datos y generación de reportes gráficos, así como recomendaciones de libros mejor valorados por género.

---

## Versiones y dependencias utilizadas
```text
Package                       Version
----------------------------- -----------
asgiref                       3.8.1
contourpy                     1.3.2
cycler                        0.12.1
Django                        5.2.3
djangorestframework           3.16.0
djangorestframework_simplejwt 5.5.0
fonttools                     4.58.4
kiwisolver                    1.4.8
matplotlib                    3.10.3
numpy                         2.3.1
packaging                     25.0
pandas                        2.3.0
pillow                        11.3.0
pip                           25.1.1
psycopg2-binary               2.9.10
PyJWT                         2.9.0
pyparsing                     3.2.3
python-dateutil               2.9.0.post0
pytz                          2025.2
seaborn                       0.13.2
six                           1.17.0
sqlparse                      0.5.3
tzdata                        2025.2
```
---

## Instalación del entorno y del proyecto

```bash
# Crear y activar entorno virtual
python -m venv venv
venv\Scripts\activate   # En Windows
```

## Instalar dependencias
pip install -r requirements.txt

## Crear proyecto Django
```bash
django-admin startproject biblioteca
cd biblioteca
python manage.py startapp libros
```

## Creacion de la base de datos
Crear la base de datos en postgresql.

Desde pgAdmin o la consola de postgresql:
```sql
CREATE DATABASE biblioteca;
CREATE USER postgres WITH PASSWORD '123';  -- Usá tu propia contraseña
GRANT ALL PRIVILEGES ON DATABASE biblioteca TO postgres;
```

## Configurar la conexión en Django (settings.py)
Abrí biblioteca/settings.py y buscá la sección DATABASES, reemplazala por:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'biblioteca',
        'USER': 'postgres',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
Una vez configurado, aplicar las migraciones correspondientes:
```bash
python manage.py makemigrations
python manage.py migrate
```
## ¿De qué trata la aplicación?
La aplicación Biblioteca es una API REST desarrollada con Django y Django REST Framework, que permite:

- Gestionar libros, autores y géneros literarios.

- Permitir que usuarios registrados califiquen libros con un puntaje decimal entre 0.5 y 5.0.

- Obtener listados y detalles de libros, autores y géneros.

- Generar recomendaciones de libros mejor valorados por género.

- Generar reportes gráficos de calificaciones, distribuciones y tendencias usando pandas, seaborn y matplotlib.

Es ideal para bibliotecas, lectores, o proyectos académicos que requieran análisis de datos sobre literatura y usuarios.

## ¿Cómo funciona?
¿Cómo funciona?
Los usuarios se registran y autentican usando JWT (Simple JWT).

Cada usuario puede calificar libros una sola vez, gracias a una restricción en el modelo.

Se pueden obtener:

- Todos los libros

- Libros filtrados por ID

- Listas de autores y géneros

Los administradores pueden:

- Agregar nuevos libros, autores, géneros

- Editar o eliminar entradas

Se pueden correr scripts personalizados para:

- Generar gráficos

- Sugerir libros por género y calificación

## Prueba de la API
En Postman

Para Registrar:
```http
POST http://127.0.0.1:8000/api/register/
```
Debe pasarse el JSON en el body:
```json
{
  "username": "blanca",
  "email": "blanca@gmail.com",
  "password": "123456"
}
``` 
![Image](https://github.com/user-attachments/assets/5efa5503-202e-4abf-a136-0c1e7a0177fa)

Para Iniciar Sesion:
```http
POST http://127.0.0.1:8000/api/login/
```
Debe pasarse las credenciales en el JSON en el body:
```json
{
  "username": "blanca",
  "password": "123456"
}
```
![Image](https://github.com/user-attachments/assets/152db9cc-fe60-4491-8f8d-3572e96530ba)

Si las credenciales son correctas se genera un token para autenticar las demas funciones.

## Prueba Api Libros
### Listar todos los libros
```http
GET http://127.0.0.1:8000/api/libros/
```
Se debe pasar el token generado en el login.
![Image](https://github.com/user-attachments/assets/06f014fd-5482-4228-b368-3e572d356ab5)

Codigo para listar todos los libros:
```python
def get(self, request):
        libros = Libro.objects.all()
        serializer = LibroSerializer(libros, many=True)
        return Response(serializer.data)
```

### Obtener libro por ID
```http
GET http://127.0.0.1:8000/api/libros/1/
```
Se debe pasar el token generado en el login.

![Image](https://github.com/user-attachments/assets/95638ae1-1902-43a4-895b-e86e1f0c32b8)

Codigo para obtener libro por ID:

```python
def get(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        serializer = LibroSerializer(libro)
        return Response(serializer.data)
```

### Insertar Libro
```http
POST http://127.0.0.1:8000/api/libros/
```
Se debe pasar el token generado en el login.

![Image](https://github.com/user-attachments/assets/c0118ceb-cec7-4650-9ad8-8710b4f66e41)

Codigo para Insertar Libro:

```python
def post(self, request):
        serializer = LibroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### Actualizar Libro
```http
PUT http://127.0.0.1:8000/api/libros/36/
```
Se debe pasar el token generado en el login.

![Image](https://github.com/user-attachments/assets/a6d3d052-d002-42c0-91a5-f359751556cb)

Codigo para Actualizar Libro:

```python
def put(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        serializer = LibroSerializer(libro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### Eliminar Libro
```http
DELETE http://127.0.0.1:8000/api/libros/36/
```
Se debe pasar el token generado en el login.

![Image](https://github.com/user-attachments/assets/065a8fff-9ed3-4c24-9a22-11d5fa24ab30)

Codigo para Eliminar Libro:

```python
def delete(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        libro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

## Análisis y Visualización de Datos
El proyecto incluye un script para generar 10 reportes gráficos basados en los datos de libros, calificaciones, usuarios, autores y géneros.

## Ubicación del script
El archivo está ubicado en:
```bash
libros/management/commands/generar_reportes.py
```

Podés ejecutarlo con:
```
python manage.py generar_reportes
```

Esto generará las imágenes .png dentro de una carpeta reportes_png/ ubicada en la raíz del proyecto.

### Gráficos generados y su interpretación
## 1. Distribución general de puntajes
Archivo: reporte1_puntajes.png
Explicación:
Muestra cómo se distribuyen los puntajes que los usuarios han dado a los libros. Permite ver si las calificaciones tienden a ser bajas, medias o altas.

![Image](https://github.com/user-attachments/assets/f4113473-9ce6-4897-8533-4fa672f861ff)

## 2. Top 10 libros mejor calificados
Archivo: reporte2_libros_top.png
Explicación:
Gráfico de barras con los 10 libros con mayor puntaje promedio. Ideal para identificar los libros más valorados por los usuarios.

![Image](https://github.com/user-attachments/assets/497b4e27-6cc0-4dce-88c2-a7777590dd73)

## 3. Puntaje promedio por género
Archivo: reporte3_genero_promedio.png
Explicación:
Muestra el puntaje promedio de todos los libros dentro de cada género. Ayuda a comparar qué género tiene mejor recepción entre los lectores.

![Image](https://github.com/user-attachments/assets/e9ace26b-3755-42c4-9e22-9cf9b3d85312)

## 4. Autores con más libros
Archivo: reporte4_autores_mas_libros.png
Explicación:
Cantidad de libros registrados por autor. Sirve para ver qué autores tienen mayor producción en la base de datos.

![Image](https://github.com/user-attachments/assets/09ddcef4-f813-4558-a1d1-2934e593ed11)

## 5. Libros con más calificaciones
Archivo: reporte5_libros_mas_calificaciones.png
Explicación:
Lista los libros que recibieron más calificaciones, lo que puede indicar popularidad o alto nivel de participación de los usuarios.

![Image](https://github.com/user-attachments/assets/9434a0d5-8133-4263-91b6-9abf0ef1b82e)

## 6. Usuarios que más califican
Archivo: reporte6_usuarios_mas_califican.png
Explicación:
Muestra los usuarios que han calificado más libros. Útil para conocer a los usuarios más activos.

![Image](https://github.com/user-attachments/assets/d39eec1f-52f8-4914-a099-88c8e772ad66)

## 7. Usuarios con puntaje promedio más alto
Archivo: reporte7_usuarios_promedio.png
Explicación:
Promedio de puntajes dados por cada usuario. Permite identificar a los usuarios más exigentes o generosos.

![Image](https://github.com/user-attachments/assets/ddeeec24-5f05-4f4f-a043-c0467bd56360)

## 8. Puntaje promedio por año de publicación
Archivo: reporte8_promedio_anio.png
Explicación:
Línea temporal que muestra cómo varía la calificación promedio según el año de publicación de los libros.

![Image](https://github.com/user-attachments/assets/ab93dffe-2156-4b26-a492-08780e288634)

## 9. Distribución de calificaciones por género
Archivo: reporte9_calificaciones_genero.png
Explicación:
Gráfico circular que muestra cuántas calificaciones pertenecen a cada género. Da una idea de en qué géneros los usuarios participan más.

![Image](https://github.com/user-attachments/assets/dc1b47d9-6b3f-45e2-b82d-338a89d39a4d)

# 10. Mapa de calor (heatmap) de correlaciones
Archivo: reporte10_heatmap.png
Explicación:
Muestra correlaciones entre variables numéricas como el puntaje promedio, cantidad de calificaciones y año de publicación. Útil para análisis más técnicos.

![Image](https://github.com/user-attachments/assets/bcf8ba54-f330-471b-9198-516eacdb2a8f)

## Recomendaciones por género
La aplicación cuenta con un script personalizado para generar en consola una lista de los libros mejor valorados de un género específico, ordenados por su puntaje promedio.

## Ubicación del script
```bash
libros/management/commands/libros_por_genero.py
```
## ¿Cómo se ejecuta?
Desde la terminal:
```bash
python manage.py libros_por_genero <ID_DEL_GENERO>
```
Ejemplo:
```bash
python manage.py libros_por_genero 3
```
Esto mostrará en la consola los 10 libros con mejor promedio de calificación pertenecientes al género con ID 3.

![Image](https://github.com/user-attachments/assets/56cb443d-6c37-422a-b5b9-9aedf54a9d4f)

## ¿Qué hace el script?
- Recibe un genero_id como argumento (por ejemplo: Romance, Ciencia ficción...).

- Busca los libros que pertenecen a ese género.

- Calcula el promedio de calificaciones que recibió cada libro.

- Ordena los libros por su puntaje promedio (de mayor a menor).

- Imprime los 10 primeros en consola con su respectivo promedio.


## Licencia

Este proyecto está licenciado bajo los términos de la [Licencia MIT](./LICENSE).

## Licencia de Terceros
```text
Name                           Version      License
 Django                         5.2.3        BSD License
 PyJWT                          2.9.0        MIT License
 asgiref                        3.8.1        BSD License
 contourpy                      1.3.2        BSD License
 cycler                         0.12.1       BSD License
 djangorestframework            3.16.0       BSD License
 djangorestframework_simplejwt  5.5.0        MIT License
 fonttools                      4.58.4       MIT
 kiwisolver                     1.4.8        BSD License
 matplotlib                     3.10.3       Python Software Foundation License
 numpy                          2.3.1        BSD License
 packaging                      25.0         Apache Software License; BSD License
 pandas                         2.3.0        BSD License
 pillow                         11.3.0       UNKNOWN
 psycopg2-binary                2.9.10       GNU Library or Lesser General Public License (LGPL)
 pyparsing                      3.2.3        MIT License
 python-dateutil                2.9.0.post0  Apache Software License; BSD License
 pytz                           2025.2       MIT License
 seaborn                        0.13.2       BSD License
 six                            1.17.0       MIT License
 sqlparse                       0.5.3        BSD License
 tzdata                         2025.2       Apache Software License
```





