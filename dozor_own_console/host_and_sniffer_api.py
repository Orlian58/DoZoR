import requests
from requests.exceptions import Timeout
import json
from functools import wraps
import re

def exeption(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.Timeout:
            return {'Устройство недоступно'}
        except json.JSONDecodeError:
            return {'Никого нет, постучите попозже'}
        except Exception as ex:
            return {'error'}
    return wrapper

@exeption
def start_sniffer(name):
    requests.get(f'http://{name}:5000/start', timeout=1).json()
    return {'Осведомитель внедрён'}

@exeption    
def stop_sniffer(name):
    requests.get(f'http://{name}:5000/stop', timeout=1).json()
    return {'Я устал, я ухожу'}
@exeption    
def sniffer_status(name):
    requests.get(f'http://{name}:5000/status', timeout=1).json()
    return {'К службе готов'}

@exeption
def select_sniffer_alerts(name, date):
    response = requests.get(f'http://{name}:5000/get_alerts?date={date}', timeout=1)
    if response == '{}':
        return {'Атак нет, можно спать спокойно'}
    alerts = []
    for item in response.split('/n'):
        alerts.append(json.loads(item))
    messages = []
    for alert in alerts:
        message = f'{alert["time"]}: {"msg"}'
        messages.append(message)
    return message

@exeption
def host_select_logs(name):
    response = requests.get(f'http://{name}:80/yara', timeout=1).json()
    logs = response["data"]
    if logs == "":
        return {'Логи очищены'}
    else:
        result = re.findall(r"<(.*)>", logs)
        logs = []
        for i in result:
            log = {}
            str = i.split('<', 1)[1].split('>', 1)[0]
            for item in str.split():
                key, value = item.split("=")
                log[key.strip("'")] = value.strip()
            logs.append(log)
        return logs

@exeption
def host_antivirus(name):
    response = requests.get(f'http://{name}:80/yara', timeout=1).json()
    viruses = response["data"]
    if viruses == "":
        return {'Вирусов нет'}
    else:
        viruses.json()
        return viruses