from django.db import models


class Alcaldia(models.Model):
    name = models.CharField(max_length=200, unique=True, db_index=True)

    def __str__(self):
        return f"<{self.id}: {self.name}>"


class UsoConstruccion(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)

    def __str__(self):
        return f"<{self.id}: {self.name}>"


class CatastroInfo(models.Model):
    alcaldia = models.ForeignKey(Alcaldia, on_delete=models.PROTECT)
    uso_construccion = models.ForeignKey(
        UsoConstruccion, on_delete=models.PROTECT
    )
    codigo_postal = models.CharField(max_length=32, db_index=True)
    superficie_terreno = models.FloatField()
    superficie_construccion = models.FloatField()
    valor_suelo = models.FloatField()
    subsidio = models.FloatField()
