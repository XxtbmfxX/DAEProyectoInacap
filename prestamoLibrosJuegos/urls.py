from django.urls import path
from . import views
from .views import CustomLogoutView


urlpatterns = [
    # path("login/", views.login_page, name="login"),
    # path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("", views.landing_page, name="home"),
    path("crear-prestamo/", views.crear_prestamo, name="crear_prestamo"),
    path("listar-pretamos/", views.listar_prestamos, name="listar_prestamos"),
    # path("crear-alumno/", views.crear_alumno, name="crear_alumno"),
    path("testing/", views.testing, name="testing"),
]
