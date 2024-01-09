from flask import Flask, render_template, request
from multiprocessing import Process
import subprocess
import os
import json
from sys import argv

app = Flask(__name__)

process = None


@app.route('/start', methods=['GET'])
def start():
    msg = {}

    #iface = request.args.get('iface')
    #iface = 'ens33'
    global process
    try:
        process = subprocess.Popen(['venv/bin/python3', 'src/Simple-NIDS.py', 'rules/exampleRules.txt', iface])
        msg['status'] = 'ok'
        return json.dumps(msg)
    except ValueError:
        return json.dumps(msg)     
    
@app.route('/stop', methods=['GET'])
def stop():
    msg = {}
    global process
    if process is not None:
        process.terminate()
        process = None
        msg['status'] = 'ok'
        return json.dumps(msg)
    else:
        return json.dumps(msg)

@app.route('/status', methods=['GET'])
def status():
    msg = {}
    global process
    if process is not None:
        msg['status'] = 'ok'
        return json.dumps(msg)
    else:
        return json.dumps(msg)

@app.route('/get_alerts', methods=['GET'])
def get_alerts():
    date = request.args.get('date') 
    files_log = os.listdir('./logs') 
    print(files_log)
    for file_name in files_log:
        if date in file_name:
            with open('./logs/' + file_name, 'r', encoding='utf-8') as file:
                alerts = file.read()
                return alerts
    return json.dumps({})

@app.route('/', methods=['GET'])
def index():
    return 'Hello world'


script, iface = argv


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)