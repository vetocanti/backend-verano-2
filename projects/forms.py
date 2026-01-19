from django import forms
from .models import Proyecto, Hito, Tarea, Subtarea

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ["nombre", "descripcion", "fecha_inicio", "fecha_termino", "participantes", "jefe_proyecto"]
        widgets = {
            "fecha_inicio": forms.DateInput(attrs={"type": "date"}),
            "fecha_termino": forms.DateInput(attrs={"type": "date"}),
        }

class HitoForm(forms.ModelForm):
    class Meta:
        model = Hito
        fields = ["nombre", "descripcion", "fecha_inicio", "fecha_termino"]
        widgets = {
            "fecha_inicio": forms.DateInput(attrs={"type": "date"}),
            "fecha_termino": forms.DateInput(attrs={"type": "date"}),
        }

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ["titulo", "descripcion", "responsable", "fecha_inicio", "fecha_termino"]
        widgets = {
            "fecha_inicio": forms.DateInput(attrs={"type": "date"}),
            "fecha_termino": forms.DateInput(attrs={"type": "date"}),
        }

class SubtareaForm(forms.ModelForm):
    class Meta:
        model = Subtarea
        fields = ["texto"]

