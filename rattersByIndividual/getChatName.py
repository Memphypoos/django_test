import requests
import configparser

# -------------------------#
# Declare Variables
# -------------------------#
character = ''

# -------------------------#
# Exchange charID for Name
# -------------------------#
def get_char_name(char_id):
  req = requests.get("https://esi.evetech.net/latest/characters/"+str(char_id))
  if req.status_code == 200: return req.json()["name"]
