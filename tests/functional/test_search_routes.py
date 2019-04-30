import pytest


@pytest.mark.usefixtures("client", "init_config_reader")
class TestSeach:

    def test_text_search(self, client, init_config_reader):
        resp = client.get('/search/green')
        assert resp.status_code == 200

    def test_get_search(self, client, init_config_reader):
        resp = client.get('/search/?value=green')
        assert resp.status_code == 200

    def test_get_search_limit(self, client, init_config_reader):
        resp = client.get('/search/?value=green&limit=2')
        assert resp.status_code == 200

