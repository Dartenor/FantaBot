import requests, json, time, utils

TIME_NOW = int(time.time() * 1000)
START_TIME = TIME_NOW - (5 * 60 * 1000)
mercato_id = '0'

def apriBuste(session, firstTime):
    mercato_id = utils.getMercatoId(session, False)
    if mercato_id == utils.REDIRECT:
        return False
    elif mercato_id == utils.MERCATO_NON_TROVATO:
        return True
        
    try:
        response = session.get('https://leghe.fantacalcio.it/servizi/V1_LegheMercatoMovimenti/lista?alias_lega=fantaoverit&id_mercato=' + str(mercato_id) + '&page_size=5000&page=0', verify=False)
        if response.status_code != 200:
            utils.exitWithMessage(session,'Error during retrieve list phase:\n' + response.text)
            
        data = json.loads(response.text)
        if not data['error_msgs'] is None and firstTime:
            return False
        
    except Exception as err:
        utils.exitWithMessage(session,'Error during retrieve list phase:\n' + str(err))
    
    movimentiAll = data['data']['Movimenti']
    calciatori = data['data']['Calciatori']
    movimentiBuste = []
    for i in range(0, len(movimentiAll)):
        if movimentiAll[i]['tipo'] == 6 and movimentiAll[i]['data'] > START_TIME:
            movimentiBuste.append(movimentiAll[i])
            
    with open("fantateams.json",'r') as teamFile:    
        teams = json.load(teamFile)

    for movimento in movimentiBuste:
        calciatoreId = int(movimento['calciatori_m'])
        for calciatore in calciatori:
            if calciatore['id'] == calciatoreId:
                movimento['player'] = calciatore
        teamId = int(movimento['id_squadra_m'])
        for team in teams['data']:
            if team['id'] == teamId:
                movimento['team'] = team

    message = 'Aperte le buste per la tornata odierna:'

    if len(movimentiBuste) == 0:
        message = message + '\n--Nessuna busta presente--'
    else:
        for movimento in movimentiBuste:
            message = message + '\n' + movimento['player']['r'] + ' ' +  movimento['player']['n'] + ' (' + movimento['player']['s'] + ') a ' + movimento['team']['nome'] + ' per ' + str(movimento['costo_m'])

    message = message + '\n\n(Le eventuali buste terminate in parità non sono presenti in questa lista)'  
    utils.sendMessage(session, message) 
    return True

session = utils.getSession()
result = apriBuste(session, firstTime=True)
if not result:
    utils.login(session)
    apriBuste(session, firstTime=False)