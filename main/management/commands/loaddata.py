from django.core.management.base import BaseCommand
from main.models import Program, Immobilier, Caracteristic
import os
import json


class Command(BaseCommand):
    help = 'Load data from json file'

    def add_arguments(self, parser):
        parser.add_argument('jsonFile_name', type=str, help='json file')


    def handle(self, *args, **kwargs):
        json_file = kwargs["jsonFile_name"]
        if json_file not in list((os.listdir())):
            print("\n\n\n###  **  Please provide the jsonfile on root folder to load data  **  ###\n\n\n")
        
        with open(json_file, "r") as reader:
            data = json.loads(reader.read())
        
        for app in data:
            print("###   **  name =>  {}     --      state =>  {}  **  ###".format(app["name"],app["state"]))

            program = Program(name=app["name"], state=app["state"]) 
            program.save()        

            for building in app["buildings"]:
                immo = Immobilier(
                    surface = building["surface"],
                    prix = building["prix"],
                    nb_pieces = building["nb_pieces"],
                    program_id=program
                )
                immo.save()
                for option in building["caracteristic"]:
                    caracteristic = Caracteristic.objects.get_or_create(option=option)[0]
                    immo.caracteristic.add(caracteristic.id) 
                immo.save()
            print("===> Data was well  added \n")

