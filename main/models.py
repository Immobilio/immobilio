from django.db import models
from django.db.models import Q, F
from django.db.models.functions import Concat




class Program(models.Model):
    state = models.BooleanField()
    name = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return f"{self.name}  --  {self.state}"


class Caracteristic(models.Model):
    option = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return f"{self.option}"


class Immobilier(models.Model):

    surface = models.FloatField()
    prix = models.FloatField()
    nb_pieces = models.IntegerField()
    caracteristic = models.ManyToManyField(Caracteristic)
    program_id = models.ForeignKey(Program, on_delete=models.CASCADE)

    @property
    def program_name(self):
        return self.program_id.name

    @property
    def options(self):
        return [carac.option for carac in self.caracteristic.all()]

    def __str__(self):
        return f"{self.program_id.name}   --  {self.prix}"

    
class PromoManager(models.Manager):
    def get_queryset(self):
        objects = super(PromoManager, self).get_queryset().all().annotate(
                    promo_prix=F("prix") * 0.95,
                    promo_program_name=Concat(F("program_id__name"), models.Value(" PROMO SPECIALE"))
                ).values("promo_prix", "promo_program_name","prix","program_id","nb_pieces","caracteristic","surface", "caracteristic")

        for object in objects:
            object['program_name'] = object.pop('promo_program_name')
            object['prix'] = object.pop('promo_prix')
            object['options'] = object.pop('caracteristic')

        return objects


class PromoImmobilierView(Immobilier):
    objects = PromoManager()
    class Meta:
        proxy = True

    def __str__(self):
        return f"{self.program_id.name}   --  PROMO SPECIALE"