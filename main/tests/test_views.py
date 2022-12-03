from django import urls
import pytest

@pytest.mark.parametrize('param', [
    ('program-list'),
    # ('program:program-detail', kwargs={"id":1}),
    ('immobilier-list'),
])
def test_render_views(client, param):
    temp_url = urls.reverse(param)
    resp = client.get(param)
    print(resp.status_code)