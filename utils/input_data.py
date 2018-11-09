from sys import version_info
from datetime import datetime

def get_value():
    if version_info.major == 3:
        return input()
    elif version_info.major == 2:
        return raw_input()

def name_now():
    ts = str(datetime.now()).split(' ')
    date = ''.join(ts[0].split('-'))
    hour = ''.join(ts[1].split(':')).split('.')[0]
    date_s = date + '_' + hour
    return date_s