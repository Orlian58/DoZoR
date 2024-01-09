from flask import Flask, request, jsonify
from functools import wraps
from waitress import serve
from json import load
import os, logging

from dissectp import artifact, yara
from arg_parser import dissect_parser, yara_parser

app = Flask(__name__)
PATH_TO_CONF = "conf/dozor.conf"

try:
    if not os.path.isfile(PATH_TO_CONF):
        raise("Файл конфигурации отсутствует")
    
    with open(PATH_TO_CONF, 'r') as CONF:
        CONF = load(CONF)
    
    if not os.path.isdir(CONF['PATH_TO_OUTPUT']):
            raise UserWarning("Некорректный путь вывода")
    
except Exception:
    raise UserWarning("Ошибка формата файла конфигуриции")


def exeption(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except UserWarning as war:
            return jsonify({'status':'error', 'msg': str(war.args[0])})
        except FileExistsError:
            return jsonify({'status':'error', 'msg': f"Такая директория уже существует"})
        except Exception as ex:
            logging.error(str(ex))
            return jsonify({'status':'error', 'msg':f'Ошибка: {ex}'})
    return wrapper


@app.route('/dissect')
@exeption
def dissect():
    arg = dissect_parser(request.args, CONF)
    
    path_to_output = CONF['PATH_TO_OUTPUT'] + str(arg["hash"])
    os.mkdir(path_to_output)

    sova = artifact(arg, path_to_output)

    return jsonify({'status':'ok', 'msg':'Dissect запущен', 'data': sova})


@app.route('/yara')
@exeption
def yaras():
    arg = yara_parser(request.args, CONF)
    
    path_to_output = CONF['PATH_TO_OUTPUT'] + str(arg["hash"])
    os.mkdir(path_to_output)

    sova = yara(arg, path_to_output, CONF['PATH_TO_YARA'])

    return jsonify({'status':'ok', 'msg':'Yara запущен', 'data': sova})


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=80)