from httpx import Timeout

from argilla_sdk import Argilla


class TestHTTPClient:

    def test_create_default_client(self):

        http_client = Argilla().http_client

        assert http_client is not None
        assert http_client.base_url == "http://localhost:6900"
        assert http_client.timeout == Timeout(60)
        assert http_client.headers["X-Argilla-Api-Key"] == "argilla.apikey"

    def test_create_client_with_custom_timeout(self):

        http_client = Argilla(timeout=30).http_client

        assert http_client is not None
        assert http_client.base_url == "http://localhost:6900"
        assert http_client.timeout == Timeout(30)
        assert http_client.headers["X-Argilla-Api-Key"] == "argilla.apikey"

    def test_create_client_with_custom_api_url(self):

        http_client = Argilla(api_url="http://localhost:8000").http_client

        assert http_client is not None
        assert http_client.base_url == "http://localhost:8000"

    def test_create_client_with_custom_api_key(self):

        http_client = Argilla(api_key="custom.apikey").http_client

        assert http_client is not None
        assert http_client.base_url == "http://localhost:6900"
        assert http_client.headers["X-Argilla-Api-Key"] == "custom.apikey"

    def test_create_client_with_extra_headers(self):

        http_client = Argilla(headers={"X-Custom-Header": "Custom value"}).http_client

        assert http_client is not None
        assert http_client.base_url == "http://localhost:6900"
        assert http_client.headers["X-Argilla-Api-Key"] == "argilla.apikey"
        assert http_client.headers["X-Custom-Header"] == "Custom value"

    def test_create_client_with_extra_cookies(self):

        http_client = Argilla(cookies={"session": "session_id"}).http_client

        assert http_client is not None
        assert http_client.base_url == "http://localhost:6900"
        assert http_client.headers["X-Argilla-Api-Key"] == "argilla.apikey"
        assert http_client.cookies["session"] == "session_id"
