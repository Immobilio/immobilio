from rest_framework import serializers
from .models import Program, Immobilier, Caracteristic
from django.db import transaction



class ProgramSerializer(serializers.ModelSerializer):

    class Meta:
        model = Program
        fields = '__all__'



class ImmobilierSerializer(serializers.ModelSerializer):

    program_name = serializers.CharField()
    options = serializers.ListField()
    program_id = serializers.IntegerField(read_only=True, source='program.id')

    class Meta:
        model = Immobilier
        fields = [field.name for field in Immobilier._meta.fields if field != "caracteristic"] 
        fields += ["program_name", "options", "surface"]


    def create(self, validated_data, *args, **kwargs):
        program = Program.objects.get(pk=validated_data["program_id"])

        immo = Immobilier.objects.filter(
            prix=validated_data["prix"],
            surface=validated_data["surface"],
            nb_pieces=validated_data["nb_pieces"],
            program_id=program.id
        )
        if immo.count() > 0:
            return {"details": "This immobilier is already stored"}

        try:
            # We need to use Transaction here to insure the creation of both Departments + Caracteristics
            with transaction.atomic():
                immo = Immobilier(
                    surface = validated_data["surface"],
                    prix = validated_data["prix"],
                    nb_pieces = validated_data["nb_pieces"],
                    program_id=program
                )
                immo.save()
                for option in validated_data["options"]:
                    caracteristic = Caracteristic.objects.get_or_create(option=option)[0]
                    immo.caracteristic.add(caracteristic.id)
                immo.save()

            validated_data["id"] = immo.id
            return validated_data
            
        except Exception as err:
            return {"error": str(err)}

        