from flask import Flask
from flask import render_template
import threading
import time

app = Flask(__name__)

#import foo_api

#api = foo_api.API('API KEY')
class ThreadingEvaluation(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval
        thread2 = threading.Thread(target=self.run, args=())
        thread2.daemon = True                            # Daemonize thread
        thread2.start()                                  # Start the execution

    def run(self):
        geocode = 1
        while True:
            geocode = 1
            print("hola")
            time.sleep(1)
            """ Method that runs forever """
        

@app.route('/')
def get_data():
    #events = api.call(get_event, arg0, arg1) 
    return render_template('index2.html', geocode=geocode)
if __name__ == "__main__":
    evaluation = ThreadingEvaluation()
    app.run()
