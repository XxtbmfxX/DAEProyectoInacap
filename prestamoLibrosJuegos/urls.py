from django.urls import path
from . import views
from .views import CustomLogoutView


urlpatterns = [
    path("", views.bienvenida, name="bienvenida"),
    path("login/", views.login_page, name="login"),
    # path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("home/", views.landing_page, name="home"),
    path("create/", views.crear_prestamo_view, name="crear_prestamo"),
    # path("read/", views.read_clientes, name="read_clientes"),
    # path("update/<int:pk>/", views.update_cliente, name="update_cliente"),
    # path("delete/<int:pk>/", views.delete_cliente, name="delete_cliente"),
    path("testing/", views.testing, name="testing"),
]
