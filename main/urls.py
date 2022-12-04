from django.urls import path
from .views import (    ProgramView, ImmobilierView, 
                        get_actif_programs, get_specific_price, get_piscine, 
                        promo_request, specific
                    )
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register('program', ProgramView, basename="program")
router.register('immobilier', ImmobilierView, basename="immobilier")


urlpatterns = router.urls