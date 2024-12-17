from django.contrib import admin
from .models import Alumno, Libro, JuegoDeMesa, Prestamo, HistorialPrestamos


# # Forma Corta
# admin.site.register(JuegoDeMesa)

# Forma extendida
# class JuegoDeMesaAdmin(admin.ModelAdmin):
#     list_display = (
#         "nombre",
#         "jugadores",
#         "prestado",
#     )  # Campos que se muestran en la lista
#     search_fields = ("nombre",)  # Campo de búsqueda
#     list_filter = ("prestado",)  # Filtros en el panel lateral
#     ordering = ("nombre",)  # Ordenar por nombre

# admin.site.register(JuegoDeMesa, JuegoDeMesaAdmin)


# Forma Sencilla
@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "apellido", "rut")
    search_fields = ("nombre", "apellido", "rut")


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "prestado")
    list_filter = ("prestado",)
    search_fields = ("titulo", "autor")


@admin.register(JuegoDeMesa)
class JuegoDeMesaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "prestado")
    list_filter = ("prestado",)
    search_fields = ("nombre",)


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = (
        "alumno",
        "fecha_inicio",
        "fecha_termino",
        "libro",
        "juego",
    )
    list_filter = ("fecha_inicio", "fecha_termino")
    search_fields = ("alumno__nombre", "elemento__nombre")


# @admin.register(HistorialPrestamos)
# class HistorialPrestamosAdmin(admin.ModelAdmin):
#     list_display = ("alumno", "elemento", "fecha_inicio", "fecha_termino")
#     list_filter = ("fecha_inicio", "fecha_termino")
#     search_fields = ("alumno__nombre", "elemento__nombre")
