## Precio agregado por m²

Desarrollo de una API demo para obtener el precio agregado (promedio, máximo y mínimo) por m2 dado un código postal de la alcaldía Álvaro Obregón utilizando datos del Gobierno de la Ciudad de México.

### API

El folder `api/` contiene un proyecto basado en Django y RESTFramework, el cual implementa la API para el obtener los precios agregados mediante el endpoint

> `GET /price-m2/zip-codes/{zip_code}/aggregate/{max|min|avg}?construction_type={1-7}`.

Para más detalle ir al [README](api/README.md) de la API.

### Ejecutar con Docker-Compose

Si se tiene instalado docker y docker-compose, es posible ejecutar un entorno similar al de producción ejecutando en la raíz del proyecto:

> $ docker compose up

Para cerrar los contenedores, presionar `Ctrl-C` y ejecutar:

> $ docker compose down

El contenedor de la API expone los servicios en el puerto 8000. Por ejemplo, se puede hacer un request hacia la siguiente URL:

> GET http://localhost:8000/price-m2/zip-codes/01219/aggregate/avg?construction_type=4

El requests puede ser hecho directamente desde el _browser_, usando _cURL_ o usando _HTTPie_.

* Con _cURL_

> $ curl 'localhost:8000/price-m2/zip-codes/01219/aggregate/avg?construction_type=4'

* Con _HTTPie_

> $ http ':8000/price-m2/zip-codes/01219/aggregate/avg?construction_type=4'
