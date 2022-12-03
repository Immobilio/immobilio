from django.shortcuts import render
from .serializers import ProgramSerializer, ImmobilierSerializer
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Program, Immobilier, PromoImmobilierView, Caracteristic
from django.db.models import Q
import datetime



MAPPING_SAISON = {
    1: "HIVER",
    2: "HIVER",
    3: "HIVER",
    4: "",
    5: "",
    6: "ETE",
    7: "ETE",
    8: "ETE",
    9: "ETE",
    10: "",
    11: "",
    12: ""
}


class ProgramView(ViewSet):
    """
    Program's viewset all programs.
    """
    serializer_class = ProgramSerializer
    http_method_names = ["post", "get","put","patch","delete"]

    def list(self, request, *args, **kwargs):
        queryset = Program.objects.all()
        serializer = ProgramSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Program.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ProgramSerializer(user)
        return Response(serializer.data)


class ImmobilierView(ViewSet):
    """
    Buildings viewset all programs.
    """
    serializer_class = ImmobilierSerializer
    http_method_names = ["post", "get","put","patch","delete"]

    def list(self, request, *args, **kwargs):
        queryset = Immobilier.objects.all()
        serializer = ImmobilierSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Immobilier.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ImmobilierSerializer(user)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        payload = request.data
        program_name = payload.get("program_name")
        options = payload.get("options")

        for field in ["prix", "surface", "nb_pieces", "program_name"]:
            if field not in list(payload.keys()):
                return Response(data={"details": f"Please provide '{field}' for this immobilier"})
        if not options or len(options) != 2:
            return Response(data={"details": "Please add exactly two options for this immobilier"})

        try:
            program = Program.objects.filter(name=program_name)[0]
            payload["program_id"] = program.id
        except:
            return Response(data={"details": f"This program '{program_name}' is not found"})

        try:
            response = ImmobilierSerializer().create(payload)
            return Response(data=response, status=200)
        except Exception as err:
            return Response(data=str(err))
        


def get_actif_programs():
    return Immobilier.objects.filter(
        Q(prix__gte=100000) and Q(prix__lte=180000)
    )
    

def get_specific_price():
    return Immobilier.objects.filter(
        Q(prix__gte=100000) and Q(prix__lte=180000)
    )


def get_piscine():
    return Immobilier.objects.filter(
        caracteristic__option="piscine",
    )


def promo_request(code_promo, query=None):
    if code_promo == "PERE NOEL":
        immos = PromoImmobilierView.objects.all()

        return immos


def specific():
    date = datetime.datetime.utcnow()
    
    if MAPPING_SAISON[date.month] == "HIVER":
        try:
            ski_option = Caracteristic.objects.filter(option="proche station ski")[0]
        except:
            ski_option = -1

        immos = Immobilier.objects.all().prefetch_related("caracteristic")
        query = list(immos.filter(Q(caracteristic__id=ski_option.id)).order_by("-prix", "-surface")) + list(immos.filter(~Q(caracteristic__id=ski_option.id)))

    elif MAPPING_SAISON[date.month] == "ETE":
        try:
            piscine_option = Caracteristic.objects.filter(option="piscine")[0]
        except:
            piscine_option = -1
        immos = Immobilier.objects.all().prefetch_related("caracteristic")
        query = list(immos.filter(Q(caracteristic__id=piscine_option.id)).order_by("-prix", "-surface")) + list(immos.filter(~Q(caracteristic__id=piscine_option.id)))

    else:
        return list(Immobilier.objects.all().prefetch_related("caracteristic").order_by("-prix", "-surface"))

    return query

