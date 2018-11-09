from flask import Flask, request
import requests
import json
import time

data = {'hostname':None,'port':None}
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def main():
    print("Welcome")
    return "Welcome!"

@app.route('/subscribe/<host>',methods=['GET'])
def subscribe(host):
    parts = host.split(":")
    data['hostname'] = parts[0]
    data['port'] = parts[1]
    print(data)
    
    return ''

@app.route('/notify',methods=['NOTIFY'])
def notify():
    print('notify')
    return json.dumps({'html':'<span>notify</span>'})

@app.route('/signUp',methods=['POST'])
def signUp():
    test= json.dumps( {'number': 12524, 'type': 'issue', 'action': 'show'} )
    headers = {'CONTENT-TYPE': 'application/json', 'CONTENT-LENGTH': str(len(test)), 'stnp-plugin': 'stnp-plugin'}
    r = requests.request('NOTIFY', 'http://'+data["hostname"]+':'+data["port"]+'/notify', data=test, headers=headers)
    print(r.status_code, r.reason)
    return ''

if __name__ == "__main__":
    app.run()
