import json
import requests
import configparser
from requests.auth import HTTPBasicAuth

#These are the Eve Developer API keys used to authenticate
config = configparser.ConfigParser()
config.read("config.ini")
eve_client = config.get("config", "eve_client")
eve_secret_key = config.get("config", "eve_secret_key")
refresh_token = config.get("config","refresh_token")
corp_id = config.get("config","corporation_id")
login_server = config.get("config", "login_server")
slack_token = config.get("config","slack_token")
scopes = config.get("config", "scopes")
authcode = config.get("config", "auth_code")
corp_id = config.get("config", "corp_id")

#Constructs the initial URL for the scopes
def constructUrl(login_server, eve_client, scopes):
  login_url = login_server+eve_client+"&scope="+scopes
  print(login_url) 

#request authorization code, to exchange for refresh code
def requestAuthCode(authcode):
  req = requests.post('https://login.eveonline.com/oauth/token', auth=HTTPBasicAuth(eve_client,eve_secret_key), data={'grant_type':'authorization_code','code': str(authcode)}).json()
  print(req)

# This function refreshes the users access and provides a new ACCESS_CODE using the REFRESH_CODE.
def refresh_esi_token(refresh_token):
 req = requests.post('https://login.eveonline.com/oauth/token', auth=HTTPBasicAuth(eve_client,eve_secret_key), data={'grant_type':'refresh_token','refresh_token': str(refresh_token)})
 if req.status_code == 200:
   return req.json()["access_token"]
   global access_token
   print("success")
 else:
   print(req.json())

def slack_key():
  config = configparser.ConfigParser()
  config.read("config.ini")
