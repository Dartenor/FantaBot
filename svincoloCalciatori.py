import requests, json, time, utils

TIME_NOW = int(time.time() * 1000)
START_TIME = TIME_NOW - (5 * 60 * 1000)
mercato_id = '0'

def cercaSvincolati(session, firstTime): 
    mercato_id = utils.getMercatoId(session, True)
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
        if movimentiAll[i]['tipo'] == 1 and movimentiAll[i]['data'] > START_TIME:
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

    if len(movimentiBuste) == 0:
        return True
       
    message = ''
    for movimento in movimentiBuste:
        message = message + 'Svincolato ' + movimento['player']['r'] + ' ' +  movimento['player']['n'] + ' (' + movimento['player']['s'] + ') da ' + movimento['team']['nome'] + '\n'
    utils.sendMessage(session, message) 
    return True

session = utils.getSession()
result = cercaSvincolati(session, firstTime=True)
if not result:
    utils.login(session)
    cercaSvincolati(session, firstTime=False)