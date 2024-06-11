## API: price-m²

A continuación veremos las maneras de iniciar el procesod de desarrollo de la API.

### Python environment

Para simplificar el manejo de las dependencias, se recomienda trabajar con Python environments.

Para crear un environment en el directorio actual, ejecutar:

```sh
$ python -m venv <ENV_NAME>
```

Para activar el environment, es necesario ejecutar el script adecuado para tu shell.
Si tu shell es Bash/Sh[^1], puedes activar el environment con el script `<ENV_NAME>/bin/activate` mediante:

```sh
$ source /path/to/<ENV_NAME>/bin/activate
```

[^1]: Dentro del mismo directorio `/bin` podrás encontrar los scripts `activate.fish` y `activate.csh`.
Necesitarás de alguno de ellos si tu shell es _Fish_ o _Csh_.

### Instalar dependencias

Este proyecto usa [Poetry](https://python-poetry.org) para gestionar las dependencias y el empaquetamiento de la API.
Con tu environment activado, instala _poetry_ con:

```sh
(env) $ pip install poetry
```

Ahora, el directorio raíz para el proyecto es el mismo donde se encuentra `pyproject.toml`[^2] o `poetry.lock`.
Para instalar las dependencias en el environment, necesitaremos estar en el directorio raíz con `cd api/` y ejecutar:

```sh
(env) $ poetry install --no-root
```

[^2]: En el archivo `pyproject.toml` encontrarás todas las dependencias, tanto para producción como para desarrollo.

### Quickstart

Necesitarás fijar el working directory en `api/construction` donde se encuentra el archivo `manage.py`.

```sh
$ cd api/construction

$ python manage.py migrate
$ python manage.py loaddata price-m2_base
$ python manage.py price-m2_pull-prices-to-db
$ python manage.py runserver 0.0.0.0:8000
```

Ahora ya estás listo para desarrollar 😎. Podrás ejecutar las consultas como:

```sh
$ curl 'localhost:8000/price-m2/zip-codes/01219/aggregate/avg?construction_type=4'
$ http ':8000/price-m2/zip-codes/01219/aggregate/avg?construction_type=4'
```

Puedes obtener la documentación de la API en formato Swagger o Redoc abriendo las siguientes URLs en el navegador:

* swagger: [http://localhost:8000/price-m2/doc/schema/swagger-ui/](http://localhost:8000/price-m2/doc/schema/swagger-ui/)
* redoc: [http://localhost:8000/price-m2/doc/schema/redoc/](http://localhost:8000/price-m2/doc/schema/redoc/)

Puedes descargar la documentación de la API en formato [OpenAPI](https://spec.openapis.org/oas/latest.html) con la URL [http://localhost:8000/price-m2/doc/schema/download](http://localhost:8000/price-m2/doc/schema/download).

### Detalle de los comandos usados

#### manage.py migrate

Actualiza el esquema de datos en la db. Por defecto creará `db.sqlite3` en el mismo folder que `manage.py`.

En el caso del contenedor de Docker, la conexión se hace a una db Postgres. Se puede modificar los settings
para usar el de producción fijando la variable de entorno `DJANGO_SETTINGS_MODULE`:

```sh
# en bash
$ export DJANGO_SETTINGS_MODULE=construction.settings.production
$ python manage.py migrate

# en fish
$ set -x DJANGO_SETTINGS_MODULE construction.settings.production
$ python manage.py migrate
```

El módulo settings por defecto es el de development `DJANGO_SETTINGS_MODULE=construction.setting.development`.

#### manage.py loaddata price-m2\_base

Ejecuta el [django-fixture](https://docs.djangoproject.com/en/5.0/topics/db/fixtures/) `construction/price_m2/fixtures/price-m2_base.yaml`.
Este contiene la lista de alcaldías y los uso-construcción que serán usadas para asociar los catastro-info.

#### manage.py price-m2\_pull-prices-to-db

Este django-command descarga la información de catastro de la alcaldía de Álvaro Obregón desde [la web](https://sig.cdmx.gob.mx/datos/#d_datos_cat) con lo datos del gobierno de La Ciudad de México. Luego de la descarga, el comando actualiza la base de datos para establecer los valores del modelo [`price_m2.models.CatastroInfo`](construction/price_m2/models.py).

#### manage.py runserver 0.0.0.0:8000

Lanza el servidor de desarrollo en el puerto 8000. La máscara "0.0.0.0" es para que puedas consultar la API desde cualquier cliente como localhost, 127.0.0.1, \<tu-ip-privada\>, \<tu-ip-pública\>, \<tu-virtual-host\>, etc.

### Despliegue en producción

Este proyecto está pensado para desplegarse usando [`gunicorn`](https://gunicorn.org/). Los pasos son los siguientes:

```sh
$ cd api/construction

$ python manage.py migrate
$ python manage.py loaddata price-m2_base
$ python manage.py price-m2_pull-prices-to-db

$ sudo gunicorn --bind 0.0.0.0:80 - construction.wsgi:application
```

Notar el uso de `sudo` debido al uso del puerto `80`.
