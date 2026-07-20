import json
import os
import pytest
import requests
from utils.DataProvider import read_json_data
from utils.DataProvider import read_excel_data
from datamodels.Product import Product
from routes.Routes import Routes
from dataclasses import asdict


json_path= os.path.abspath(os.path.join(os.path.dirname(__file__),"../testdata/productdata.json"))
xl_path= os.path.abspath(os.path.join(os.path.dirname(__file__),"../testdata/products_data.xlsx"))

class TestProductAPI:
    @pytest.fixture(autouse=True)
    def init_class_var(self, setup):
        self.base_url = setup["base_url"]
        self.config = setup["config_reader"]

    # @pytest.mark.parametrize("product_test_data", read_json_data(json_path))
    @pytest.mark.parametrize("product_test_data", read_excel_data(xl_path, "products_data"))
    def test_add_new_delete_products(self, product_test_data):
        product_data= product_test_data

        title= product_data["title"]
        description= product_data["description"]
        price= product_data["price"]
        category= product_data["category"]
        stock= product_data["stock"]
        payload= Product(title,price,description,category,stock)

        #Create Product
        response= requests.post(self.base_url+Routes.CREATE_PRODUCT,json=asdict(payload))
        assert response.status_code == 201, "wrong status code"
        data= response.json()
        print(json.dumps(data, indent=4))
        assert data["title"]== title
        product_id = data["id"]

        #DeleteProduct
        res= requests.delete(self.base_url+Routes.DELETE_PRODUCT.format(id= product_id))
        assert res.status_code== 200, "Wrong status code"


