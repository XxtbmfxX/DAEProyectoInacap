from django.test import TestCase
from .forms import PrestamoForm
from .models import Alumno, Libro

from django.urls import reverse


class CrearAlumnoViewTest(TestCase):
    def test_renderizar_formulario(self):
        response = self.client.get(reverse("crear_alumno"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Registrar Nuevo Alumno 👨‍🎓")

    def test_crear_alumno_exitoso(self):
        data = {
            "rut": "12345678-9",
            "nombre": "Juan",
            "apellido": "Pérez",
        }
        response = self.client.post(reverse("crear_alumno"), data)
        self.assertEqual(Alumno.objects.count(), 1)  # Verificar que se creó un alumno


class PrestamoFormTest(TestCase):
    def setUp(self):
        # Crear instancias necesarias para las pruebas
        self.alumno = Alumno.objects.create(
            rut="12345678-9", nombre="Juan", apellido="Pérez"
        )
        self.libro = Libro.objects.create(
            nombre="El Principito", autor="Antoine de Saint-Exupéry", prestado=False
        )

    def test_form_valido(self):
        data = {
            "alumno": self.alumno.id,
            "elemento": self.libro.id,
            "fecha_prestamo": "2024-12-16 10:00",
        }
        form = PrestamoForm(data)
        self.assertTrue(form.is_valid())  # Verifica que el formulario sea válido

    def test_form_invalido(self):
        data = {
            "alumno": "",  # Falta un alumno válido
            "elemento": self.libro.id,
            "fecha_prestamo": "2024-12-16 10:00",
        }
        form = PrestamoForm(data)
        self.assertFalse(form.is_valid())  # El formulario debería ser inválido

    def test_elemento_no_disponible(self):
        # Marcar el libro como prestado
        self.libro.prestado = True
        self.libro.save()

        data = {
            "alumno": self.alumno.id,
            "elemento": self.libro.id,
            "fecha_prestamo": "2024-12-16 10:00",
        }
        form = PrestamoForm(data)
        self.assertFalse(
            form.is_valid()
        )  # El formulario debería ser inválido porque el libro está prestado
