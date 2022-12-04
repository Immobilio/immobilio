from django import urls
import pytest
from main.views import *



@pytest.mark.django_db
def test_get_actif_programs(client):
    queryset = get_actif_programs()
    for instance in queryset:
        assert instance.program_id.state == 1


@pytest.mark.django_db
def test_get_specific_price(client):
    queryset = get_specific_price()
    for instance in queryset:
        assert instance.prix >= 100000.00 and instance.prix <= 180000.00


@pytest.mark.django_db
def test_get_piscine(client):
    queryset = get_piscine()
    for instance in queryset:
        assert "piscine" in instance.caracteristic.all()


@pytest.mark.django_db
def test_promo_request(client):
    normal_instances = PromoImmobilierView.objects.all()
    queryset = promo_request(code_promo="PERE NOEL")
    
    for discount_instance,normal_instance in zip(queryset, normal_instances):
        assert normal_instance.program_name.endswith("PROMO SPECIALE")
        assert discount_instance.price == normal_instance.price * 0.95
