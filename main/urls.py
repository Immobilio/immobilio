from django.urls import path
from .views import (    ProgramView, ImmobilierView, 
                        get_actif_programs, get_specific_price, get_piscine, 
                        promo_request, specific
                    )
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register('program', ProgramView, basename="program")
router.register('immobilier', ImmobilierView, basename="immobilier")


urlpatterns = [
    path("get_actif_programs", get_actif_programs, name="get_actif_programs"),
    path("get_specific_price", get_specific_price, name="get_specific_price"),
    path("get_piscine", get_piscine, name="get_piscine"),
    path("promo_request", promo_request, name="promo_request"),
    path("specific", specific, name="specific")
] + router.urls