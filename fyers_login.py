import configparser
from fyers_api import fyersModel
from fyers_api import accessToken
from fyers_api.websocket import ws
from selenium import webdriver
import urllib.parse as urlparse
import time
from selenium.webdriver.chrome.options import Options
import pandas as pd
import pdb

config = configparser.ConfigParser()
config.read('credential.ini')

app_id = config['fyers']['app_id']
app_secret = config['fyers']['app_secret']
redirect_url = config['fyers']['redirect_url']
user_id = config['fyers']['user_id']
password = config['fyers']['password']
two_fa = config['fyers']['two_fa']


class Fyers:
    
    def __init__(self,app_id,app_secret,redirect_url,user_id,password,two_fa):
        self.app_id = app_id
        self.app_secret = app_secret
        self.redirect_url = redirect_url
        self.user_id = user_id
        self.password = password
        self.two_fa = two_fa
        self.set_token()
        
    def get_session_url(self):
        self.session = accessToken.SessionModel(client_id=self.app_id,
                                            secret_key=self.app_secret,
                                            redirect_uri=self.redirect_url,
                                            response_type='code', 
                                            grant_type='authorization_code')
        self.url = self.session.generate_authcode()
        print('generating url successful')
        # print(f'current url: {self.url}')

    def login_driver(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=options)

        driver.get(self.url)
        user_name = driver.find_element_by_id("fyers_id")
        pass_word = driver.find_element_by_id("password")
        pan_card = driver.find_element_by_id("pancard")
        submit_button = driver.find_element_by_id("btn_id")

        user_name.send_keys(user_id)
        pass_word.send_keys(password)
        pan_card.send_keys(two_fa)
        submit_button.click()
        time.sleep(5)
        print('chrome driver fatch successful')
        return driver

    def get_auth_code(self,driver):
        current_url = driver.current_url
        driver.quit()
        parsed = urlparse.urlparse(current_url)
        auth_code = urlparse.parse_qs(parsed.query)['auth_code'][0]
        print(f'auth code generated successful ')
        return auth_code

    def set_token(self):
        global access_token
        self.get_session_url()
        driver = self.login_driver()
        auth_code = self.get_auth_code(driver)
        self.session.set_token(auth_code)
        response = self.session.generate_token()
        access_token = response['access_token']
        print(f'access token generated successful')
        self.fyers = fyersModel.FyersModel(client_id=app_id, token=access_token, log_path='log')  #, log_path='log'

fyers = Fyers(app_id,app_secret,redirect_url,user_id,password,two_fa)
print('Login Successful')