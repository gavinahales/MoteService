from flask import Flask, request, abort
from mote import Mote

app = Flask(__name__)
#If a mote isn't connected the app falls over at this point.
#mote = Mote()

@app.route('/motestatus/', methods=['GET'])
def lightstatusreq():
    if request.method == 'GET':
        #TO BE IMPLEMENTED
        return 'This will return the current status of the lights.'
    else:
        abort(405)

@app.route('/setmote/', methods=['POST'])
def setmotereq():
    if request.method == 'POST':
        #TO BE IMPLEMENTED
        return 'This will set the Mote lights'
    else:
        abort(405)

#USED FOR DEVELOPMENT ON WINDOWS ONLY. REMOVE WHEN COMPLETE
if __name__ == '__main__':
    app.run()
