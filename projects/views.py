from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from .models import Proyecto, Hito, Tarea, Subtarea
from .forms import ProyectoForm, HitoForm, TareaForm, SubtareaForm
from django.contrib.auth import logout



@login_required
@permission_required("core.view_proyecto", raise_exception=True)
def proyecto_list(request):
    # Participante verá solo los proyectos donde está como participante
    qs = Proyecto.objects.all()
    if request.user.groups.filter(name="PARTICIPANTE").exists():
        qs = qs.filter(participantes=request.user)
    return render(request, "core/proyecto_list.html", {"proyectos": qs})


@login_required
@permission_required("core.add_proyecto", raise_exception=True)
def proyecto_create(request):
    if request.method == "POST":
        form = ProyectoForm(request.POST)
        if form.is_valid():
            proyecto = form.save()
            # opcional: auto-incluir creador como participante
            proyecto.participantes.add(request.user)
            return redirect("proyecto_list")
    else:
        form = ProyectoForm()
    return render(request, "core/proyecto_form.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("proyecto_list")
    # Implementación del login
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("proyecto_list")
    else:
        form = AuthenticationForm()
    return render(request, "core/login.html", {"form": form})

@login_required
def logout_view(request):
    # Implementación del logout
    logout(request)
    return redirect("login")

@login_required
@permission_required("core.view_proyecto", raise_exception=True)
def proyecto_detail(request, pk):
    proyecto = Proyecto.objects.prefetch_related("hitos__tareas__subtareas").get(pk=pk)
    hitos = proyecto.hitos.all()
    hito_form = HitoForm()
    tarea_form = TareaForm()
    subtarea_form = SubtareaForm()
    return render(request, "core/proyecto_detail.html", {
        "proyecto": proyecto,
        "hitos": hitos,
        "hito_form": hito_form,
        "tarea_form": tarea_form,
        "subtarea_form": subtarea_form,
    })


@login_required
@permission_required("core.change_proyecto", raise_exception=True)
def proyecto_edit(request, pk):
    proyecto = Proyecto.objects.get(pk=pk)
    if request.method == "POST":
        form = ProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
            return redirect("proyecto_detail", pk=proyecto.pk)
    else:
        form = ProyectoForm(instance=proyecto)
    return render(request, "core/proyecto_form.html", {"form": form, "proyecto": proyecto})

@login_required
@permission_required("core.add_proyecto", raise_exception=True)
def create_hito(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    if request.method == "POST":
        form = HitoForm(request.POST)
        if form.is_valid():
            hito = form.save(commit=False)
            hito.proyecto = proyecto
            hito.save()
            return redirect("proyecto_detail", pk=proyecto.pk)
    return redirect("proyecto_detail", pk=proyecto.pk)

@login_required
@permission_required("core.add_proyecto", raise_exception=True)
def create_tarea(request, proyecto_pk, hito_pk):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_pk)
    hito = get_object_or_404(Hito, pk=hito_pk, proyecto=proyecto)
    if request.method == "POST":
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.hito = hito
            tarea.save()
            return redirect("proyecto_detail", pk=proyecto.pk)
    return redirect("proyecto_detail", pk=proyecto.pk)

@login_required
@permission_required("core.add_proyecto", raise_exception=True)
def create_subtarea(request, proyecto_pk, hito_pk, tarea_pk):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_pk)
    hito = get_object_or_404(Hito, pk=hito_pk, proyecto=proyecto)
    tarea = get_object_or_404(Tarea, pk=tarea_pk, hito=hito)
    if request.method == "POST":
        form = SubtareaForm(request.POST)
        if form.is_valid():
            subtarea = form.save(commit=False)
            subtarea.tarea = tarea
            subtarea.save()
            return redirect("proyecto_detail", pk=proyecto.pk)
    return redirect("proyecto_detail", pk=proyecto.pk)

# EDITAR HITO
@login_required
@permission_required("core.change_proyecto", raise_exception=True)
def edit_hito(request, proyecto_pk, hito_pk):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_pk)
    hito = get_object_or_404(Hito, pk=hito_pk, proyecto=proyecto)
    if request.method == "POST":
        form = HitoForm(request.POST, instance=hito)
        if form.is_valid():
            form.save()
            return redirect("proyecto_detail", pk=proyecto.pk)
    else:
        form = HitoForm(instance=hito)
    return render(request, "core/hito_form.html", {"form": form, "hito": hito, "proyecto": proyecto})

# ELIMINAR HITO
@login_required
@permission_required("core.delete_proyecto", raise_exception=True)
def delete_hito(request, proyecto_pk, hito_pk):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_pk)
    hito = get_object_or_404(Hito, pk=hito_pk, proyecto=proyecto)
    if request.method == "POST":
        hito.delete()
        return redirect("proyecto_detail", pk=proyecto.pk)
    return render(request, "core/confirm_delete.html", {"object": hito, "type": "hito"})

# EDITAR TAREA
@login_required
@permission_required("core.change_proyecto", raise_exception=True)
def edit_tarea(request, proyecto_pk, hito_pk, tarea_pk):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_pk)
    hito = get_object_or_404(Hito, pk=hito_pk, proyecto=proyecto)
    tarea = get_object_or_404(Tarea, pk=tarea_pk, hito=hito)
    if request.method == "POST":
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            return redirect("proyecto_detail", pk=proyecto.pk)
    else:
        form = TareaForm(instance=tarea)
    return render(request, "core/tarea_form.html", {"form": form, "tarea": tarea, "proyecto": proyecto})

# ELIMINAR TAREA
@login_required
@permission_required("core.delete_proyecto", raise_exception=True)
def delete_tarea(request, proyecto_pk, hito_pk, tarea_pk):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_pk)
    hito = get_object_or_404(Hito, pk=hito_pk, proyecto=proyecto)
    tarea = get_object_or_404(Tarea, pk=tarea_pk, hito=hito)
    if request.method == "POST":
        tarea.delete()
        return redirect("proyecto_detail", pk=proyecto.pk)
    return render(request, "core/confirm_delete.html", {"object": tarea, "type": "tarea"})

# EDITAR SUBTAREA
@login_required
@permission_required("core.change_proyecto", raise_exception=True)
def edit_subtarea(request, proyecto_pk, hito_pk, tarea_pk, subtarea_pk):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_pk)
    hito = get_object_or_404(Hito, pk=hito_pk, proyecto=proyecto)
    tarea = get_object_or_404(Tarea, pk=tarea_pk, hito=hito)
    subtarea = get_object_or_404(Subtarea, pk=subtarea_pk, tarea=tarea)
    if request.method == "POST":
        form = SubtareaForm(request.POST, instance=subtarea)
        if form.is_valid():
            form.save()
            return redirect("proyecto_detail", pk=proyecto.pk)
    else:
        form = SubtareaForm(instance=subtarea)
    return render(request, "core/subtarea_form.html", {"form": form, "subtarea": subtarea, "proyecto": proyecto})

# ELIMINAR SUBTAREA
@login_required
@permission_required("core.delete_proyecto", raise_exception=True)
def delete_subtarea(request, proyecto_pk, hito_pk, tarea_pk, subtarea_pk):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_pk)
    hito = get_object_or_404(Hito, pk=hito_pk, proyecto=proyecto)
    tarea = get_object_or_404(Tarea, pk=tarea_pk, hito=hito)
    subtarea = get_object_or_404(Subtarea, pk=subtarea_pk, tarea=tarea)
    if request.method == "POST":
        subtarea.delete()
        return redirect("proyecto_detail", pk=proyecto.pk)
    return render(request, "core/confirm_delete.html", {"object": subtarea, "type": "subtarea"})

# TOGGLE SUBTAREA
@login_required
@permission_required("core.view_proyecto", raise_exception=True)
def toggle_subtarea(request, proyecto_pk, hito_pk, tarea_pk, subtarea_pk):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_pk)
    hito = get_object_or_404(Hito, pk=hito_pk, proyecto=proyecto)
    tarea = get_object_or_404(Tarea, pk=tarea_pk, hito=hito)
    subtarea = get_object_or_404(Subtarea, pk=subtarea_pk, tarea=tarea)
    subtarea.completada = not subtarea.completada
    subtarea.save()
    return redirect("proyecto_detail", pk=proyecto.pk)



