import requests, json, sys, pickle, urllib3, os

BOT_URL = 'https://api.telegram.org/bot951165628:AAEGyfy3tK5enLaN_rSaDvOW5-hn97UZ5AY/'
#group_chat_id = '-1001423004582'
group_chat_id = '543935138'
dev_chat_id = '543935138'
cookieFile = 'cookies.dmp'
appkeyFile = 'appKey.dmp'

def save_cookies(session):
    with open(cookieFile, 'wb') as f:
        pickle.dump(session.cookies, f)

def load_cookies():
    try:
        if os.path.exists(cookieFile):
            with open(cookieFile, 'rb') as f:
                return pickle.load(f)
        return None
    except Exception:
        return None
        
def save_appkey(appkey):
    with open(appkeyFile, 'w') as f:
        f.write(appkey)

def load_appkey(): 
    try:
        if os.path.exists(appkeyFile):
            with open(appkeyFile, 'r') as f:
                return f.read()
        return None
    except Exception:
        return None

def getSession():
    session = requests.Session()
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'})
    appkey = load_appkey()
    if not appkey is None:
        session.headers.update({'app_key' : appkey})
    
    cookies = load_cookies()
    if not cookies is None:
        session.cookies.update(cookies)
    return session

def exitWithMessage(session, message):
    json_data = {
        "chat_id": dev_chat_id,
        "text": message,
    }
    session.post(BOT_URL + 'sendMessage', json=json_data, verify=False)
#    print(message)
    sys.exit()
    
def login(session):    
    try:
        response = session.get('https://leghe.fantacalcio.it/', verify=False)
        index = response.text.find('authAppKey')
        app_key = response.text[index +13:index+13+40]
        save_appkey(app_key)    
        session.headers.update({'app_key': app_key})

        jsonLogin = {'password':'Dartenor;85','username':'Daniele_BO'}
        response = session.put('https://leghe.fantacalcio.it/api/v1/v1_utente/login?alias_lega=fantaoverit',json=jsonLogin, verify=False)
        if response.status_code != 200:
            exitWithMessage(session, 'Error during login phase:\n' + response.text)
            
        save_cookies(session) 
    except Exception as err:
        exitWithMessage(session, 'Error during login phase:\n' + str(err)) 
        
def sendMessage(session, message):
    json_data = {
        "chat_id": group_chat_id,
        "text": message,
    }
    session.post(BOT_URL + 'sendMessage', json=json_data, verify=False)
    
def getMercatoId(session):
    try:
        response = session.get('https://leghe.fantacalcio.it/fantaoverit/area-gioco/mercato-buste', verify=False)
        if response.status_code == 302:
            return -2
        
        if response.status_code != 200:
           exitWithMessage(session,'Error during retrieve list phase:\n' + response.text)
            
        indexStart = response.text.find('Object moved')
        if indexStart >= 0:
            return -2
        
        indexStart = response.text.find('id_mercato')    
        if indexStart < 0:
            return -1   
        
        indexEnd = response.text.find(',', indexStart) 
        
        return int(response.text[indexStart+12:indexEnd])
        
    except Exception as err:
        exitWithMessage(session,'Error during retrieve market phase:\n' + str(err))