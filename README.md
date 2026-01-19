# backend-verano-2

Guía rápida para levantar el proyecto Django con MySQL.

## Requisitos
- Python 3.10+ y pip
- MySQL 8 (u otra variante compatible con el conector `mysqlclient`)
- (Opcional) `virtualenv` o `venv` para aislar dependencias

## Paso a paso
1. Clona el repositorio y entra al directorio.
2. Crea y activa un entorno virtual (opcional pero recomendado).
3. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Crea tu archivo `.env` (ver sección siguiente).
5. Ejecuta migraciones:
   ```bash
   python manage.py migrate
   ```
6. (Opcional) Crea un superusuario:
   ```bash
   python manage.py createsuperuser
   ```
7. Levanta el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

## Variables de entorno
El proyecto lee la configuración desde un archivo `.env` si está instalado `python-dotenv`, o desde las variables del sistema en producción. Usa el ejemplo para crear el tuyo:

```bash
cp .env.example .env
```

Variables esperadas:
```
SECRET_KEY=clave-secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_ENGINE=django.db.backends.mysql
DB_NAME=project_db
DB_USER=root
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=3306
```

Para producción pon `DEBUG=False`, ajusta `ALLOWED_HOSTS` (dominios/ips permitidos) y usa credenciales seguras.

## Comandos útiles
- Aplicar migraciones pendientes: `python manage.py migrate`
- Crear superusuario: `python manage.py createsuperuser`
- Correr servidor: `python manage.py runserver`

## Notas
- El archivo [.env.example](.env.example) queda como plantilla; no lo modifiques en producción, copia a `.env`.
- Si necesitas servir archivos estáticos en producción, configura `STATIC_ROOT` y ejecuta `python manage.py collectstatic`.
