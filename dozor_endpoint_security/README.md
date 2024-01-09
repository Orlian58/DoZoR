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

1) Для запуска на конечной точке Dozor Endpoint Security требует установки [Python](https://www.python.org/downloads/release/python-31013/) v3.10+  и virtualenv текущей версии.
2) Для работы антивирусного сканера необходимо добавить yara правила к примеру https://github.com/Yara-Rules/rules.git по пути PATH_TO_YARA (по умолчанию по пути /opt/yara-repo/).
3) Установить путь до файла с конфигурацией dozor.conf в вашей системе(по умолчанию: conf/dozor.conf) в файле flask-api/app/app.py (в переменную PATH_TO_CONF (по умолчанию conf/dozor.conf)

For production environments...
```bash
cd dozor_endpoint_security/
./install.sh
sudo su
source venv/bin/activate
python flask-api/app/app.py &
```
После запуска настроить конфигурацию dozor.conf:

"HASH_RANGE":"99999999", - максимальный диопазон постфикса временых файлов
"OUTPUT_PREFIX":"DOZOR_", - превикс временых файлов
"PATH_TO_IMAGE": "/", - - путь определяющий корень сканируемой файловой системы
"PATH_TO_OUTPUT": "/home/ubuntu/Desktop/", - путь до рабочей директории
"PATH_TO_YARA": "/opt/yara-repo/", - путь до используемых yara правил

"DISSECT":{"images":"/","hash":"None","param":"authlog,securelog,syslog"},
"YARA":{"images":"/","hash":"None","path":"/","rule":"","size":"99999999999999999"},