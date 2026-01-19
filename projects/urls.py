from django.urls import path
from . import views

urlpatterns = [
    path("proyectos/", views.proyecto_list, name="proyecto_list"),
    path("proyectos/nuevo/", views.proyecto_create, name="proyecto_create"),
    path("proyectos/<int:pk>/", views.proyecto_detail, name="proyecto_detail"),
    path("proyectos/<int:pk>/editar/", views.proyecto_edit, name="proyecto_edit"),
    path("proyectos/<int:pk>/hito/nuevo/", views.create_hito, name="create_hito"),
    path("proyectos/<int:proyecto_pk>/hito/<int:hito_pk>/editar/", views.edit_hito, name="edit_hito"),
    path("proyectos/<int:proyecto_pk>/hito/<int:hito_pk>/eliminar/", views.delete_hito, name="delete_hito"),
    path("proyectos/<int:proyecto_pk>/hito/<int:hito_pk>/tarea/nuevo/", views.create_tarea, name="create_tarea"),
    path("proyectos/<int:proyecto_pk>/hito/<int:hito_pk>/tarea/<int:tarea_pk>/editar/", views.edit_tarea, name="edit_tarea"),
    path("proyectos/<int:proyecto_pk>/hito/<int:hito_pk>/tarea/<int:tarea_pk>/eliminar/", views.delete_tarea, name="delete_tarea"),
    path("proyectos/<int:proyecto_pk>/hito/<int:hito_pk>/tarea/<int:tarea_pk>/subtarea/nuevo/", views.create_subtarea, name="create_subtarea"),
    path("proyectos/<int:proyecto_pk>/hito/<int:hito_pk>/tarea/<int:tarea_pk>/subtarea/<int:subtarea_pk>/editar/", views.edit_subtarea, name="edit_subtarea"),
    path("proyectos/<int:proyecto_pk>/hito/<int:hito_pk>/tarea/<int:tarea_pk>/subtarea/<int:subtarea_pk>/eliminar/", views.delete_subtarea, name="delete_subtarea"),
    path("proyectos/<int:proyecto_pk>/hito/<int:hito_pk>/tarea/<int:tarea_pk>/subtarea/<int:subtarea_pk>/toggle/", views.toggle_subtarea, name="toggle_subtarea"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
