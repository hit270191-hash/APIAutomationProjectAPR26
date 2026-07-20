import logging
import os

import pytest
import requests

from routes.Routes import Routes
from utils.ConfigReader import ReadConfig


#Path for log file
Log_file= os.path.abspath(os.path.join(os.path.dirname(__file__),"../logs/test_logging.log"))
#create log folder if it does not exist
os.makedirs(os.path.dirname(Log_file), exist_ok=True)
#create logger object
logger= logging.getLogger("api_logger")
#set logging level(DEBUG= log everything)
logger.setLevel(logging.DEBUG)

#prevent adding multiple handlers again and again
if not logger.handlers:
    #filehandler -> logs will be saved in a file
    file_handler = logging.FileHandler(Log_file, mode= 'a')
    #set log format
    formatter= logging.Formatter('%(asctime)s- %(levelname)s - %(message)s')
    #apply format to file handler
    file_handler.setFormatter(formatter)
    #attach file handler to logger
    logger.addHandler(file_handler)

def log_request_response(response: requests.Response):
    req= response.request
    logger.info(f"Request: {req.method} {req.url}")
    logger.info(f"Request Headers: {req.headers}")

    if req.body:
        logger.info(f"Request Body: {req.body}")

    logger.info(f"Response status: {response.status_code}")
    logger.info(f"Response Headers: {response.headers}")
    try:
        logger.info(f"Response Body: {response.json()}")
    except:
        logger.info(f"Response Body: {response.text}")


@pytest.fixture(scope="class")
def setup():
    #save original funtion
    #here original requests become requests session
    original_request= requests.Session.request

    #this is our own version of the request() method.
    def custom_request(self, method, url, **kwargs):
        #Call original request
        response= original_request(self, method, url, **kwargs)
        #log request and response
        log_request_response(response)
        return response

    requests.Session.request= custom_request
    '''
    
    This is done by monkey patching:
    
    Request Flow:
    requests.put==>  requests.Session.request ==> custom_request ==> original_request ==> requests.Session.request
    Response Flow:
    requests.Session.request==>original_request ==>custom_request (response) ==> requests.Session.request==> requests.put
     '''

    yield {"base_url": Routes.Base_url, "config_reader": ReadConfig}




