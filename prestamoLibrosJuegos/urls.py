from django.urls import path
from . import views
from .views import CustomLogoutView


urlpatterns = [
    path("", views.bienvenida, name="bienvenida"),
    path("login/", views.login_page, name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("home/", views.landing_page, name="home"),
    path("crear-prestamo/", views.crear_prestamo, name="crear_prestamo"),
    path("testing/", views.testing, name="testing"),
]
