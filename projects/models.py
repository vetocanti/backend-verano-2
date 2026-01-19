from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Proyecto(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    participantes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="proyectos",
        blank=True,
    )
    jefe_proyecto = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="proyectos_jefe"
    )

    def clean(self):
        if self.fecha_termino < self.fecha_inicio:
            raise ValidationError("La fecha de término no puede ser menor que la fecha de inicio.")

    def __str__(self):
        return self.nombre


class Hito(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="hitos")
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    participantes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="hitos",
        blank=True,
    )

    def clean(self):
        if self.fecha_termino < self.fecha_inicio:
            raise ValidationError("La fecha de término del hito no puede ser menor que la de inicio.")
        # Reglas respecto al proyecto
        if self.proyecto_id:
            if self.fecha_inicio < self.proyecto.fecha_inicio or self.fecha_termino > self.proyecto.fecha_termino:
                raise ValidationError("El hito debe estar dentro del rango de fechas del proyecto.")

    def __str__(self):
        return f"{self.proyecto.nombre} - {self.nombre}"


class Tarea(models.Model):
    hito = models.ForeignKey(Hito, on_delete=models.CASCADE, related_name="tareas")
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="tareas_responsable",
    )
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()

    def clean(self):
        if self.fecha_termino < self.fecha_inicio:
            raise ValidationError("La fecha de término de la tarea no puede ser menor que la de inicio.")
        # Reglas: tarea dentro del rango del hito
        if self.hito_id:
            if self.fecha_inicio < self.hito.fecha_inicio or self.fecha_termino > self.hito.fecha_termino:
                raise ValidationError("La tarea debe estar dentro del rango de fechas del hito.")

    def __str__(self):
        return f"{self.hito.nombre} - {self.titulo}"


class Subtarea(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name="subtareas")
    texto = models.CharField(max_length=255)
    completada = models.BooleanField(default=False)

    def __str__(self):
        return f"[{'X' if self.completada else ' '}] {self.texto}"
