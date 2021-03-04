from flask import Response


def default_response_tests(response: Response):
    assert response.status_code == 200
    assert response.content_type == 'application/json'
