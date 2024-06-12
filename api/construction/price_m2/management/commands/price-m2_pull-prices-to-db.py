import csv
import urllib.request
from io import BytesIO, TextIOWrapper
from zipfile import BadZipFile, ZipFile

from django.core.management import BaseCommand, CommandError
from price_m2.models import Alcaldia, CatastroInfo, UsoConstruccion


class Command(BaseCommand):
    """
    Comando para descargar y registrar en DB el CSV de catastro de la alcaldía Álvaro Obregón.
    Ver el modelo `price_m2.models.CatastroInfo` para una lista de los campos registrados.

    Cuando algunos registros del CSV no puede ser procesado, se genera un archivo
    `failed_rows.txt` en la ruta relativa a la ejecución del comando. Por cada línea,
    el archivo contiene una tupla con el mensaje de la excepción lanzada y el contenido
    del registro que causó la excepción.

    Ejemplo de uso: manage.py price-m2_pull-prices-to-db.

    Observaciones:
    * El comando lee y agrega los elementos del CSV. «NO SINCRONIZA».
      Si la tabla "CatastroInfo" ya tiene elementos, la ejecución los eliminará antes
      de registrar los nuevos elementos.
      TODO: Evaluar si la sinconización puede ir acá o es mejor tener un task a futuro.
    * Adicionalmente, se puede trabajar para que este comando deje un archivo en algún directorio
      destinado a caché; por ejemplo: ~/.cache, /tmp, /var/cache, etc.
      Como mejora, se puede validar el MD5 del archivo para confirmar si es el mismo archivo que
      el almacenado en la web `https://sig.cdmx.gob.mx/datos/#d_datos_cat` de manera que
      no sea necesario la descarga.
    * Opcionalmente al punto anterior, se puede agregar un parámetro `--csv_path`
      para usar el CSV del disco en lugar de desacargarlo.
    """

    ZIP_URL = "https://catalogo.sig.cdmx.gob.mx/documents/75/download"
    # A la fecha sólo se maneja esta cantidad de tipos de construcción
    LIMIT_USO_CONSTRUCCION = 10

    def handle(self, *_, **__):
        failed_pairs = []
        catastro_infos = []

        # TODO: De momento, manejamos sólo esta alcaldía por requerimiento.
        # Convertir a parámetro cuando se soporte más alcaldías.
        try:
            alcaldia = Alcaldia.objects.get(name="Álvaro Obregón")
        except Alcaldia.DoesNotExist:
            self.stderr.write(
                self.style.ERROR(
                    "No existe la tabla `Alcaldia` en la db. (Verificar migrate)"
                )
            )
            return
        self.stdout.write(
            self.style.WARNING(
                ">>> Agregar registros de catastro de la alcaldía Álvaro Obregón. <<<"
            )
        )

        self.stdout.write("Eliminando registros de CatastroInfo...", ending="")
        CatastroInfo.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(" OK"))

        csv_content = self._download_catastro_alvaro_obregon()

        uso_construccion_map = self._create_uso_construccion_map()

        reader = csv.DictReader(TextIOWrapper(csv_content))
        for row in reader:
            try:
                catastro_infos.append(
                    CatastroInfo(
                        alcaldia=alcaldia,
                        uso_construccion=uso_construccion_map[
                            row["uso_construccion"]
                        ],
                        codigo_postal=row["codigo_postal"],
                        superficie_terreno=float(row["superficie_terreno"]),
                        superficie_construccion=float(
                            row["superficie_construccion"]
                        ),
                        valor_suelo=float(row["valor_suelo"]),
                        subsidio=float(row["subsidio"]),
                    )
                )
            except Exception as error:
                failed_pairs.append((str(error), str(row)))

        total_items = len(failed_pairs) + len(catastro_infos)
        self.stdout.write(f"Total de elementos procesados: {total_items}")
        self.stdout.write(
            f"Total de elementos exitosos: {len(catastro_infos)}"
        )

        if failed_pairs:
            self.stdout.write(
                self.style.ERROR(
                    f"Hay {len(failed_pairs)} filas con error. Ver archivo failed-rows.txt"
                )
            )
            with open("failed_rows.txt", "w") as failed_file:
                failed_file.write("\n\n".join(str(p) for p in failed_pairs))

        if catastro_infos:
            CatastroInfo.objects.bulk_create(catastro_infos)

    def _create_uso_construccion_map(self):
        """Obtiene desde db los valores válidos para el campo `uso_construccion`

        NOTA: Nosotros usamos `Sin Zonificación` para etiquetar algunos `uso_construccion`.
        Pero en el CSV, se usa la cadena vacía "" para representar los `uso_construccion` sin zonificación.
        """
        if UsoConstruccion.objects.count() != self.LIMIT_USO_CONSTRUCCION:
            self.stderr.write(
                self.style.ERROR(
                    f"Este comando está diseñado para {self.LIMIT_USO_CONSTRUCCION} valores distintos de `uso_construccion`."
                )
            )

        uso_construccion = UsoConstruccion.objects.all()[
            : self.LIMIT_USO_CONSTRUCCION
        ]
        uso_construccion_map = {item.name: item for item in uso_construccion}
        uso_construccion_map[""] = uso_construccion_map["Sin Zonificación"]

        return uso_construccion_map

    def _download_catastro_alvaro_obregon(self) -> BytesIO:
        """
        Este método descarga el CSV de catastro de la alcaldía Álvaro Obregón.

        NOTA: Considerar que el CSV contiene 1.8 millones de registros.
        Durante las pruebas la carga funcionó bien. Pero en caso de necesitar mejorar
        este proceso, se puede manejar el registro por batches o se puede aumentar
        la infraestructura para considerar un task-queue como Huey o Celery para sincronizar
        la db con el CSV cada cierto periodo de tiempo.

        Info adicional:
        - Content-Length: 29612694
        - Tamaño: 30MB aprox
        - Formato de archivo: zip
        """
        self.stdout.write("Descargando el archivo...", ending="")
        # El comando podría usar un parámetro `path` para no descargar el csv en cada ejecución
        with urllib.request.urlopen(self.ZIP_URL) as response:

            zip_data = BytesIO(response.read())
            self.stdout.write(self.style.SUCCESS(" OK"))

            try:
                csv_content = self._read_zip_bytes(zip_data)
            except BadZipFile as error:
                raise CommandError(
                    f"El archivo devuelto por '{self.ZIP_URL}' no es un zip file."
                ) from error

            return csv_content

    def _read_zip_bytes(self, zip_data: BytesIO) -> BytesIO:
        """Retorna el contenido del CSV dentro del Zip.

        Hay una validación adicional: hasta la fecha, el zip sólo debe contener un único archivo CSV.
        Otro formato lanzará una excepción.
        """
        with ZipFile(zip_data, "r") as zip_catalog:
            filenames = zip_catalog.namelist()

            self.stdout.write("Archivos encontrados")
            for name in filenames:
                self.stdout.write(f"  - {name}")

            if len(filenames) != 1:  # el zip tiene otro formato
                raise CommandError(
                    "Hay más de un archivo. El nuevo formato necesita una actualización a este comando."
                )

            with zip_catalog.open(filenames[0]) as csv_file:
                return BytesIO(csv_file.read())
