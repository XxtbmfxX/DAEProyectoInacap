from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login
from django.contrib import messages

from .models import Prestamo, JuegoDeMesa, Libro
from .forms import PrestamoForm, LibroForm, AlumnoForm, JuegoDeMesaForm


def is_admin(user):
    return user.is_superuser


class CustomLogoutView(LogoutView):
    template_name = "logout.html"  # Opcional, un template para mostrar al cerrar sesión


# def login_page(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             messages.success(request, f"¡Bienvenido, {user.username}! 😊")
#             return redirect("home")
#         else:
#             messages.error(
#                 request,
#                 "Usuario o contraseña inválidos. Por favor, intenta nuevamente. 🙁",
#             )
#     return render(request, "login.html")


def bienvenida(request):
    return render(request, "bienvenida.html")


def landing_page(request):
    prestamos = Prestamo.objects.all()

    return render(request, "main.html",{"prestamos": prestamos})


# @login_required
# @user_passes_test(is_admin)
def crear_prestamo(request):
    if request.method == "POST":
        form = PrestamoForm(request.POST)
        if form.is_valid():
            prestamo = form.save(commit=False)
            tipo_elemento = form.cleaned_data.get("tipo_elemento")
            elemento_id = form.cleaned_data.get("elemento_id")

            if tipo_elemento == "libro":
                prestamo.libro = get_object_or_404(Libro, id=elemento_id)
                prestamo.libro.prestado = True
                prestamo.libro.save()
            elif tipo_elemento == "juego":
                prestamo.juego = get_object_or_404(JuegoDeMesa, id=elemento_id)
                prestamo.juego.prestado = True
                prestamo.juego.save()

            prestamo.save()
            messages.success(request, "¡Préstamo registrado con éxito! 📚✅")
            return redirect("landing_page")
        else:
            messages.error(
                request,
                "Error al registrar el préstamo. ❌ Verifica los datos ingresados.",
            )
    else:
        form = PrestamoForm()

    return render(request, "form_prestamo.html", {"form": form})


# @login_required
# @user_passes_test(is_admin)
# def crear_libro(request):
#     if request.method == "POST":
#         form = LibroForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Libro agregado correctamente. 📖✅")
#             return redirect("landing_page")
#         else:
#             messages.error(request, "No se pudo agregar el libro. ❌")
#     else:
#         form = LibroForm()

#     return render(
#         request,
#         "form_base.html",
#         {"form": form, "titulo": "Agregar un Nuevo Libro 📚", "boton": "Guardar Libro"},
#     )
#     # return render(request, "form_libro.html", {"form": form})


# @login_required
# def crear_alumno(request):
#     if request.method == "POST":
#         form = AlumnoForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Alumno agregado correctamente. 👨‍🎓✅")
#             return redirect(
#                 "home"
#             )  # Redirigir a la página principal después de guardar
#         else:
#             messages.error(
#                 request,
#                 "No se pudo agregar el alumno. Por favor, revisa los datos ingresados. ❌",
#             )
#     else:
#         form = AlumnoForm()

#     return render(request, "crear_alumno.html", {"form": form})


# @login_required
def listar_prestamos(request):
    # prestamos = Prestamo.objects.select_related(
    #     "alumno", "libro", "juego_de_mesa"
    # )  # Evitar consultas N+1
    prestamos = Prestamo.objects.all()
    print("="*20)
    print(prestamos)
    print("="*20)
    return render(request, "listar_prestamos.html", {"prestamos": prestamos})


def testing(request):
    return render(request, "testing.html")
