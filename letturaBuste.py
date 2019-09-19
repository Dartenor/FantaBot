import requests, json, random, sys, utils

def leggiBuste(session, firstTime):    
    try:
        response = session.get('https://leghe.fantacalcio.it/servizi/v1_legheMercatoBusta/listaBuste?alias_lega=fantaoverit&timestamp=0', verify=False)
        if response.status_code != 200:
            utils.exitWithMessage(session, 'Error during retrieve list phase:\n' + response.text)
            
        data = json.loads(response.text)
        if not data['error_msgs'] is None and firstTime:
            return False
        
    except Exception as err:
        utils.exitWithMessage(session, 'Error during retrieve list phase:\n' + str(err))
    
    if data['error_msgs'] is not None:
        errorMsg =  data['error_msgs'][0]['descrizione']
        if not errorMsg.startswith('Mercato non'):
            utils.exitWithMessage(session, 'Error during retrieve list phase:\n' + errorMsg)
    
    if data['data'] is None:
        return True

    buste = data['data']['buste']
    message = 'Giocatori validi per la tornata odierna:'

    if len(buste) == 0:
        message = message + '\n--Nessuna busta presentata--'
    else:
        random.shuffle(buste)
        for player in buste:
            message = message + '\n' + player['r'] + ' ' + player['c'] + ' (' + player['s'] + ')'
    
    utils.sendMessage(session, message)
    return True

session = utils.getSession()
result = leggiBuste(session, firstTime=True)
if not result:
    utils.login(session)
    leggiBuste(session, firstTime=False)