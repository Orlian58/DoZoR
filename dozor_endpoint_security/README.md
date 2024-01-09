# Dozor Endpoint Security

## Features

- Адаптивное rest api на flask
- Настраиваемые параметры конфигурации(сборки, пути и тд)
- Сбор большого количества артефактов OC linux
- Yara сканирование 

Dozor Endpoint Security это инструмент разработанный на python с использованием широких возможностей api библиотеки dissect. Поддерживает бльное количество источников событий и артефактов OC linux.

## Tech

- [Flask] - легковестный web сервер!
- [Dissect] - api для проффесионалов в сфере реагироваания на инциденты безопасности
- [Waitress] -  — WSGI-сервер на Python рассчитанный на работу в нагруженных системах

## Installation

Для запуска на конечной точке Dozor Endpoint Security требует установки [Python](https://www.python.org/downloads/release/python-31013/) v3.10+.

For production environments...
```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt --no-index -f dist
exit
sudo su
source venv/bin/activate
python 3 flask-api/app/app.py &
```
После запуска настроить конфигурацию dozor.conf:

"HASH_RANGE":"99999999",
"OUTPUT_PREFIX":"DOZOR_",
"PATH_TO_IMAGE": "/",
"PATH_TO_OUTPUT": "/home/ubuntu/Desktop/",
"PATH_TO_YARA": "/opt/yara-repo/",

"DISSECT":{"images":"/","hash":"None","param":"authlog,securelog,syslog"},
"YARA":{"images":"/","hash":"None","path":"/","rule":"","size":"99999999999999999"},