"""Este módulo debe contener los valores significativos
en el django-app `price_m2` definidos por el negocio.

Considerar que los services mantienen la lógica y este módulo
sólo contiene aquellos valores que son transversales a los primeros.

OBSERVACIÓN: Evaluar si estos valores deberían ser settings de usuario.
Si el usuario debe poder cambiar el comportamiento de la app, el valor
acá establecido debería moverse al módulo de configuraciones-de-usuario.
"""

# Límites para listar `models.Alcaldia`
ALCALDIA_LIMIT_WARNING = 1000
ALCALDIA_ACTUAL_LIMIT = 1700

# Límites para listar `models.UsoConstruccion`
USO_CONSTRUCCION_LIMIT_WARNING = 20
USO_CONSTRUCCION_ACTUAL_LIMIT = 50

# Mensajes del cálculo de agregación de price_m2
NO_CONSTRUCTION_FOUND_MESSAGE = "No se halló el tipo de construcción"
NO_ZIP_CODE_FOUND_MESSAGE = "No se halló el código zip solicitado"
