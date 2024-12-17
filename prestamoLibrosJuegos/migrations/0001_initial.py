# Generated by Django 5.1.3 on 2024-12-16 20:42

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(max_length=12, unique=True)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='JuegoDeMesa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('jugadores', models.IntegerField()),
                ('prestado', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Libro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('autor', models.CharField(max_length=255)),
                ('prestado', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='HistorialPrestamos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('fecha_prestamo', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date')),
                ('fecha_devolucion', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date')),
                ('alumno', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='historial_prestamos', to='prestamoLibrosJuegos.alumno')),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='Prestamo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_prestamo', models.DateTimeField()),
                ('fecha_devolucion', models.DateTimeField(blank=True, null=True)),
                ('pure', models.DateTimeField(blank=True, null=True)),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prestamoLibrosJuegos.alumno')),
                ('juego', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='prestamoLibrosJuegos.juegodemesa')),
                ('libro', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='prestamoLibrosJuegos.libro')),
            ],
        ),
    ]
