from flask import Flask, request, render_template
import requests
app = Flask(__name__)


@app.route("/")
def main():
    return render_template('index.html')

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
@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    return processed_text
if __name__ == "__main__":
    app.run()
