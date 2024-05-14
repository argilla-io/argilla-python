from unittest import mock

import argilla_sdk as rg


class TestArgilla:
    def test_default_client(self):
        with mock.patch("argilla_sdk.Argilla") as mock_client:
            mock_client.return_value.api_url = "http://localhost:6900"
            mock_client.return_value.api_key = "admin.apikey"
            mock_client.return_value.workspace = "argilla"

            client = rg.Argilla(api_url="http://localhost:6900", api_key="admin.apikey")
            assert client.api_url == "http://localhost:6900"
            assert client.api_key == "admin.apikey"


    def test_multiple_clients(self):
        with mock.patch("argilla_sdk.client._api.APIClient.http_client") as mock_client:
            local_client = rg.Argilla(api_url="http://localhost:6900", api_key="admin.apikey")
            remote_client = rg.Argilla(api_url="http://argilla.production.net", api_key="admin.apikey")
            assert local_client.api_url == "http://localhost:6900"
            assert remote_client.api_url == "http://argilla.production.net"
