import requests
import pytest
import json

from routes.Routes import Routes
from payloads.Payload import Payload

new_product_id= None

class TestProduct:
    @pytest.fixture(autouse=True)
    def init_class_var(self,setup):
        self.base_url = setup["base_url"]
        self.config = setup["config_reader"]
        self.category= "bags"
        self.payload = Payload().products_payload()

    @pytest.mark.smoke
    @pytest.mark.order(1)
    def test_get_all_products(self):
        res= requests.get(self.base_url+Routes.GET_ALL_PRODUCTS)
        assert res.status_code == 200, "Wrong status code"
        data= res.json()
        # print(json.dumps(data, indent=4))

    @pytest.mark.regression
    @pytest.mark.order(5)
    def test_get_product_by_id(self):
        # product_id= self.config.get_property("productId")       #Fetched value from config.ini file

        res= requests.get(self.base_url+Routes.GET_PRODUCT_BY_ID.format(id=new_product_id))
        assert res.status_code == 200, "Wrong status code"
        data= res.json()
        print(json.dumps(data, indent=4))

    @pytest.mark.sanity
    @pytest.mark.order(2)
    def test_get_product_by_limit(self):
        limit= self.config.get_property("limit")
        res= requests.get(self.base_url+Routes.GET_PRODUCT_BY_LIMIT.format(limit=limit))
        data= res.json()
        print(json.dumps(data, indent=4))
        assert res.status_code == 200, "Wrong status code"

    @pytest.mark.smoke
    @pytest.mark.order(3)
    def test_get_product_by_category(self):
        res = requests.get(self.base_url + Routes.GET_PRODUCT_BY_CATEGORY.format(category=self.category))
        data = res.json()
        print(json.dumps(data, indent=4))
        assert res.status_code == 200, "Wrong status code"

    @pytest.mark.regression
    @pytest.mark.order(7)
    def test_delete_product(self):
        res = requests.delete(self.base_url + Routes.DELETE_PRODUCT.format(id=new_product_id))
        assert res.status_code == 200, "Wrong status code"
        print("Product Deleted....")

    @pytest.mark.regression
    @pytest.mark.order(4)
    def test_create_product(self):
        global new_product_id
        res= requests.post(self.base_url+Routes.CREATE_PRODUCT,json=self.payload.__dict__)
        assert res.status_code == 201, "Wrong status code"
        data=res.json()
        print(json.dumps(data, indent=4))
        assert data["title"]== self.payload.__dict__["title"]
        new_product_id= data["id"]
        print("New Product Created...")

    @pytest.mark.regression
    @pytest.mark.order(6)
    def test_update_product(self):
        res= requests.put(self.base_url+Routes.UPDATE_PRODUCT.format(id=new_product_id)
                          ,json=self.payload.__dict__)
        assert res.status_code == 200, "Wrong status code"
        data=res.json()
        print(json.dumps(data, indent=4))
        assert data["title"]== self.payload.__dict__["title"]
        print("Product Updated...")


