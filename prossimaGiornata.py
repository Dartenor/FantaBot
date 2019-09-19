import requests, json, urllib3, sys, pytz, utils
from datetime import datetime, timedelta

session = requests.Session()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'})
session.headers.update({'X-Auth-Token': '5da64a93bc7d44deb43c5a5503cccabe'})

today = datetime.today()
tomorrow = today + timedelta(days=1) 
response = session.get('http://api.football-data.org/v2/competitions/SA/matches?dateFrom=' + today.strftime('%Y-%m-%d') + '&dateTo=' + tomorrow.strftime('%Y-%m-%d'))

data = response.json()
if not 'matches' in data:
    utils.exitWithMessage(session, 'ProssimoMatch Error: No matches key in json')
    
matches = data['matches']
if len(matches) == 0:
    sys.exit()

matchDay = matches[0]['matchday']
response = session.get('http://api.football-data.org/v2/competitions/SA/matches?matchday=' + str(matchDay))

data = response.json()
if not 'matches' in data:
    utils.exitWithMessage(session, 'ProssimoMatch Error: No matches key in json')
    
matches = data['matches']
if len(matches) == 0:
    sys.exit()

matchStatus = matches[0]['status']
if matchStatus != 'SCHEDULED':
    sys.exit()
    
dateString = matches[0]['utcDate']
dateMatch = datetime.strptime(dateString, '%Y-%m-%dT%H:%M:%S%z')
timezone = pytz.timezone('Europe/Rome')

dateMatch = dateMatch.astimezone(timezone)
dateNow = datetime.now().astimezone(timezone)

hoursTillMatch = (dateMatch - dateNow).total_seconds() / 60 / 60

message = '\nRicordatevi di postare la formazione almeno 15 minuti prima'

if hoursTillMatch > 23.5 and hoursTillMatch < 25.5:
    message = 'La prossima giornata inizierà domani alle ' + dateMatch.strftime('%H:%M') + message
elif hoursTillMatch > 2.5 and hoursTillMatch < 4.5:
    message = 'La prossima giornata inizierà OGGI alle ' + dateMatch.strftime('%H:%M') + message
else:
    sys.exit()

utils.sendMessage(session, message)