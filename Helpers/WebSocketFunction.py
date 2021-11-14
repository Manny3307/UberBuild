from Helpers.ExceptionLogging import UberExceptionLogging
import websocket
import json

UberLogString = []

#Create the Instance of UberExceptionLogging Functions 
objUberExceptionLogging = UberExceptionLogging()

#Load Exception Messages
ExceptionMessages = objUberExceptionLogging.load_exception_success("Exception")

#Load the Success Messages
SuccessMessages = objUberExceptionLogging.load_exception_success("Success")

#Create the web socket and send messages to client side.  
class WebSocketFunction:

    #Send message to web socket opened at the client
    def SendWSMessage(Text_Message):
        try:
            GeneralConfig = open('../Config/config.json')
            Generalconf = json.load(GeneralConfig)
            
            ws = websocket.WebSocket()
            ws.close()
            ws.connect(Generalconf["configs"]["WebSocket_URL"])
            ws.send(json.dumps({'value': Text_Message}))
        except:
            objUberExceptionLogging.UberLogException(f"ERROR: Can't create the websocket connection to {Generalconf['configs']['WebSocket_URL']}. Please check if Redis Channels are up and working", True, True)
            objUberExceptionLogging.UberLogException("ERROR: OOPs!!!! something went wrong, can't send the data to Web Socket.", True, True)