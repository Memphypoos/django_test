import configparser
import sso
import requests
from requests.auth import HTTPBasicAuth

# -------------------------#
# Declare Variables
# -------------------------#
config = configparser.ConfigParser()
config.read("config.ini")
corp_id = config.get("config", "corp_id")
refresh_token = config.get("config","refresh_token")
access_token = sso.refresh_esi_token(refresh_token)
header = {"User-Agent":"WalletAudit:Memphypoos","Authorization":"Bearer "+str(access_token)}
charID = ''

# -------------------------------------#
# Exchange corpID for list of charID's
# -------------------------------------#
def get_members(corp_id):
  memberList = []
  req = requests.get("https://esi.evetech.net/latest/corporations/"+str(corp_id)+"/members/", headers=header)
  if req.status_code == 200:
      for charID in req.json():
        memberList.append(charID)
  return(memberList)      

# -------------------------------------#
# Exchange charID for Name
# -------------------------------------#
def get_char_name(char_id):
  req = requests.get("https://esi.evetech.net/latest/characters/"+str(char_id))
  if req.status_code == 200: return req.json()["name"]


mainCharacter = {
                 'Memphis Madagascar': ['Memphy Fiddlebits', 'Pongus','Nikita Nofriends', 'Memphis Mong', 'Memphis Madagascar','Shuirath','Lord Xzib'],

                 'Lucian Thorundan': ['Death By-Lazors', 'Lucian Thorundan', 'Johnny Templars'],

                 'Ion Udan': ['Ion Udan', 'Vas Vaculik', 'Sammy Jay'],

                 'TwobitGW' : ['TwobitGW', 'oXiDe321', 'Ali3nSan', 'Aliensan', 'Mr Negoro'],

                 'Lister Dalais': ['Lister Dalais', 'Bilious McGee'],

                 'Wanto Xadi': ['Wanto Xadi', 'Anna Xadi', 'Tarou Sharvas', 'Ruken Oeko', 'Nina Chelien', 'Hanchen Wu', 'Harris Oeko', 'Junfei Lin'],

                 'Decres Rova': ['Decres Rova', 'Decres Estidal', 'Decres Wolf', 'Decres Alduin', 'Decres Draconem', 'The SalmonMoose'],

                 'Ziildjian' : ['Ziildjian', 'Madukze', 'Leesho Aishai'], 	 

                 'Ash Haakari' : ['Ash Haakari', 'Ares Achase'],

                 'Strolling Astronomer' : ['Strolling Astronomer', 'Roary Breaker'],

                 'Mal Isbad' : ['Mal Isbad', 'Jamal Melonbane', 'Malcom Rekt', 'Jamal Stereotyped'],

                 'Khanadore' : ['Khanadore', 'Jeznyat', 'Blanche Doobwa'],

                 'Ezeria Mistanta' : ['Ezeria Mistanta', 'Akiko Tammura', 'Chastity Mistanta', 'Seize-The-Means-Of Production'],
                 
                 'Quitrilis' : ['Quitrilis', 'SeriousCallers Only', 'GodMade MeDo It', 'Phelma', 'Light Messiah'],

                 'Crispyskin' : ['Crispyskin', 'uncommoncold'],

                 'Lyam260' : ['Lyam260', 'Kitsu Nakimishiwa'],

                 'DirtyHaww sixtynine' : ['DirtyHaww sixtynine'],

                 'So Suime' : ['So Suime', 'Suime So']
                 }


  

