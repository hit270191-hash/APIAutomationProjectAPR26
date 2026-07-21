from dataclasses import asdict

import requests
import pytest
from routes.Routes import Routes
from payloads.Payload import Payload
import json

cart_id=None

class TestCart:
    @pytest.fixture(autouse=True)
    def init_class_var(self,setup):
        self.base_url = setup["base_url"]
        self.config= setup["config_reader"]
        self.payload = Payload().cart_payload()

    def test_create_cart(self):
        global cart_id
        res= requests.post(self.base_url+Routes.CREATE_CART,json=asdict(self.payload))
        assert res.status_code == 201, "Wrong status code"
        data=res.json()
        print(json.dumps(data,indent=4))
        cart_id=data["id"]

