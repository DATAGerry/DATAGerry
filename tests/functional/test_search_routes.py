import pytest


@pytest.mark.usefixtures("init_config_reader")
@pytest.fixture
def config_reader(init_config_reader):
    pass


@pytest.mark.usefixtures("config_reader")
def test_text_search(client, config_reader):
    resp = client.get('/search/green')
    assert resp.status_code == 200


@pytest.mark.usefixtures("config_reader")
def test_get_search(client, config_reader):
    resp = client.get('/search/?value=green')
    assert resp.status_code == 200
