from flask import Flask, request, abort, json
from mote import Mote

app = Flask(__name__)

#Preset colours, colour tuples follow format (r, g, b, altr, altg, altb).
#Alt colours are used to create strips with 2 alternating colours.
#Set alt values to same if only single colour wanted.
COLOURPRESETS = {'lightblue':(0, 191, 255, 0, 191, 255),
                 'sunset':(255, 218, 185, 255, 218, 185)
                }

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

#Change the colour of the Mote.
def setmote(channels, red, green, blue):
    mote.clear()
    for channel in channels:
        for pixel in range(0, 16):
            mote.set_pixel(channel, pixel, red, green, blue)
    mote.show()

#Turn the Mote off completely.
def moteoff():
    mote.clear()
    mote.show()

#Check the current status of the Mote.
@app.route('/motestatus/', methods=['GET'])
def motestatusreq():
    if request.method == 'GET':
        # TO BE IMPLEMENTED
        if mote is None:
            retdata = {'MoteReply': {
                'status': '0',
                'error': 'Mote device has not been connected. Try calling connectmote.'}}
            return json.jsonify(retdata)
        else:
            # Can do this using mote.get_pixel()
            return 'This will return the current status of the lights.'
    else:
        abort(405)

#Set the colour of the Mote strips.
@app.route('/setmote/', methods=['POST'])
def setmotereq():
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            # Do something with the incoming JSON
            parsedjson = request.json

            # Try to parse the incoming JSON request.
            # The JSON object must be a MoteRequest.
            try:
                moterequest = parsedjson['MoteRequest']

                # Check what the requesttype field is set to, and respind in the following ways:
                # setmote: Change the colour of the motes specified in the JSON request.
                # moteoff: Turn all motes off.
                if moterequest['requesttype'] == "setmote":

                    # Catch any errors in case JSON is not correct or setting
                    # mote fails
                    try:
                        channels = moterequest['channels']
                        red = moterequest['red']
                        green = moterequest['green']
                        blue = moterequest['blue']
                        setmote(channels, red, green, blue)
                        retdata = {'MoteReply': {
                            'status': '1'}}
                        return json.jsonify(retdata)

                    # If this doesn't work, catch the Exception
                    # TODO: Change the exception type to something more
                    # specific
                    except Exception:
                        retdata = {'MoteReply': {
                            'status': '0',
                            'error': 'Setting mote lights failed.'}}
                        return json.jsonify(retdata)

                elif moterequest['requesttype'] == "moteoff":
                    if mote is None:
                        retdata = {'MoteReply': {
                            'status': '0',
                            'error': 'Mote device not connected.'}}
                    else:
                        moteoff()
                        retdata = {'MoteReply': {
                            'status': '1'}}
                    return json.jsonify(retdata)
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

#Try and connect to the Mote. Used if the initial connection fails.
@app.route('/connectmote/', methods=['GET, POST'])
def connectmote():
    try:
        mote = Mote()
        retdata = {'MoteReply': {
            'status': '1'}}
    except IOError:
        mote = None
        retdata = {'MoteReply': {
            'status': '0',
            'error': 'Mote device failed to connect. Check device is physically connected and try again.'}}
        return json.jsonify(retdata)


# USED FOR DEVELOPMENT ON WINDOWS ONLY. REMOVE WHEN COMPLETE
if __name__ == '__main__':
    app.run()
