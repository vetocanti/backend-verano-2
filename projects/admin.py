from django.contrib import admin
from .models import Proyecto, Hito, Tarea, Subtarea

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "jefe_proyecto", "fecha_inicio", "fecha_termino")
    search_fields = ("nombre",)
    fields = ("nombre", "jefe_proyecto", "fecha_inicio", "fecha_termino")

@admin.register(Hito)
class HitoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "proyecto", "fecha_inicio", "fecha_termino")
    list_filter = ("proyecto",)

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "hito", "responsable", "fecha_inicio", "fecha_termino")
    list_filter = ("hito", "responsable")

@admin.register(Subtarea)
class SubtareaAdmin(admin.ModelAdmin):
    list_display = ("id", "texto", "tarea", "completada")
    list_filter = ("completada",)
