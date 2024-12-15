from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from .models import Cliente
from .forms import ClienteForm


def is_admin(user):
    return user.is_superuser


# class CustomLoginView(LoginView):
#     template_name = "login.html"  # Ruta a tu template de inicio de sesión


class CustomLogoutView(LogoutView):
    template_name = 'logout.html'  # Opcional, un template para mostrar al cerrar sesión

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            error = "Usuario o contraseña inválidos. Por favor, intenta nuevamente. 🙁"
            return render(request, "login.html", {"error": error})
    return render(request, "login.html")


def bienvenida(request):
    return render(request, "bienvenida.html")


@login_required
def landing_page(request):
    return render(request, "main.html")


@login_required
@user_passes_test(is_admin)
def create_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("read_clientes")
    else:
        form = ClienteForm()
    return render(request, "create_form.html", {"form": form})


@login_required
def read_clientes(request):
    query = request.GET.get("q", "")
    if query:
        clientes = Cliente.objects.filter(nombre__icontains=query)
    else:
        clientes = Cliente.objects.all()
    return render(request, "read.html", {"clientes": clientes, "query": query})


@login_required
@user_passes_test(is_admin)
def update_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect("read_clientes")
    else:
        form = ClienteForm(instance=cliente)
    return render(request, "update_form.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def delete_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        cliente.delete()
        return redirect("read_clientes")
    return render(request, "delete_confirm.html", {"cliente": cliente})

def testing(request):
    return render(request, "testing.html")