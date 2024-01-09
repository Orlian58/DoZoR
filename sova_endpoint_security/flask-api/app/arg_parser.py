import os, re
from random import randint


def validator(args, exclude, param) -> list:
    format = r'^[\d\w_\- .]+$'

    if param in exclude:
        return [exclude[param]]
    if args is None and args == '':
        raise UserWarning(f'Параметр {param} не может быть пустым')
    
    args = re.split(',', args)

    for arg in args:
        if re.match(format, arg) is None:
            raise UserWarning(f'Ошибка формата {param}')
    return args

def agregator(mod, hash, CONF) -> str:

    if 'hash' in CONF[mod]:
        for _ in range(int(CONF['HASH_RANGE'])):
            hash = CONF['OUTPUT_PREFIX'] + str(randint(1, int(CONF['HASH_RANGE'])))
            if hash not in os.listdir():
                break
    return hash

def dissect_parser(args, CONF) -> list:

    images = validator(args.get('images'), CONF['DISSECT'], 'images')
    param = validator(args.get('param'),  CONF['DISSECT'], 'param')[0]
    hash = validator(args.get('hash'), CONF['DISSECT'], 'hash')[0]
    hash = agregator('DISSECT', hash, CONF)

    return {'hash': hash, 'targets': list(map(lambda s: CONF['PATH_TO_IMAGE'] + s, images)), 'func': param}

def yara_parser(args, CONF) -> list:
    
    images = validator(args.get('images'), CONF['YARA'], 'images')
    size = validator(args.get('size'),  CONF['YARA'], 'size')[0]
    path = validator(args.get('path'), CONF['YARA'], 'path')[0]
    hash = validator(args.get('hash'), CONF['YARA'], 'hash')[0]
    rule = validator(args.get('rule'), CONF['YARA'], 'rule')[0]
    hash = agregator('YARA', hash, CONF)

    return {'hash': hash, 'rule': rule, 'targets': list(map(lambda s: CONF['PATH_TO_IMAGE'] + s, images)), 'path': path, 'size': size}