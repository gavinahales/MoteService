from flask import Flask, request, abort, json
from mote import Mote

app = Flask(__name__)

# Try connecting to the Mote, but make sure it fails gracefully.
try:
    mote = Mote()
    mote.configure_channel(1, 16, False)
    mote.configure_channel(2, 16, False)
    mote.configure_channel(3, 16, False)
    mote.configure_channel(4, 16, False)
    mote.clear()
except IOError:
    mote = None


def setmote(channels, red, green, blue):
    mote.clear()
    for channel in channels:
        for pixel in range(0, 16):
            mote.set_pixel(channel, pixel, red, green, blue)
    mote.show()


def moteoff():
    mote.clear()
    mote.show()


@app.route('/motestatus/', methods=['GET'])
def motestatusreq():
    if request.method == 'GET':
        # TO BE IMPLEMENTED
        if mote is None:
            return 'Mote device not connected.'
        else:
            # Can do this using mote.get_pixel()
            return 'This will return the current status of the lights.'
    else:
        abort(405)


@app.route('/setmote/', methods=['POST'])
def setmotereq():
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            # Do something with the incoming JSON
            parsedjson = request.json

            ##NEEDS SOME COMMENTING
            try:
                moterequest = parsedjson['MoteRequest']

                if moterequest['requesttype'] == "setmote":
                    return "Accepted but not implemented."
                else:
                    retdata = {'MoteReply': {
                        'status': '0',
                        'error': 'Mote request not supported or malformed.'}}
                    return json.jsonify(retdata)
            except KeyError:
                retdata = {'MoteReply': {
                    'status': '0',
                    'error': 'Mote request not supported or malformed.'}}
                return json.jsonify(retdata)

        else:
            retdata = {'MoteReply': {
                'status': '0',
                'error': 'JSON expected as input.'}}
            return json.jsonify(retdata)
    else:
        abort(405)


@app.route('/connectmote/', methods=['GET, POST'])
def connectmote():
    try:
        mote = Mote()
    except IOError:
        mote = None
        return 'Mote device not found. Connect failed.'


# USED FOR DEVELOPMENT ON WINDOWS ONLY. REMOVE WHEN COMPLETE
if __name__ == '__main__':
    app.run()
