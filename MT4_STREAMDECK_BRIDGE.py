import json
from posixpath import expanduser
import threading
import subprocess
import os
from PIL import Image, ImageDraw
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper
from DWX_ZeroMQ_Connector_v2_0_1_RC8 import DWX_ZeroMQ_Connector
print(os.path.abspath(os.getcwd()))
mt4Connector = DWX_ZeroMQ_Connector( 
                 _ClientID='dwx-zeromq',    # Unique ID for this client
                 _host='localhost',         # Host to connect to
                 _protocol='tcp',           # Connection protocol
                 _PUSH_PORT=32768,          # Port for Sending commands
                 _PULL_PORT=32769,          # Port for Receiving responses
                 _SUB_PORT=32770,           # Port for Subscribing for prices
                 _delimiter=';',
                 _pulldata_handlers = [],   # Handlers to process data received through PULL port.
                 _subdata_handlers = [],    # Handlers to process data received through SUB port.
                 _verbose=False,             # String delimiter
                 _poll_timeout=1000,        # ZMQ Poller Timeout (ms)
                 _sleep_delay=0,        # 1 ms for time.sleep()
                 _monitor=False)
configFile = None

def streamDeskConnection():
    streamdecks = DeviceManager().enumerate()
    print("Found {} Stream Deck(s).\n".format(len(streamdecks)))

    for index, deck in enumerate(streamdecks):
        if(deck.open() != None):
            print("if")
            deck.close()
        else:
            print("else")
            deck.open()
            deck.reset()
        print("hello2")
        print("Opened '{}' device (serial number: '{}')".format(
            deck.deck_type(), deck.get_serial_number()))

        # Set initial screen brightness to 30%.
        deck.set_brightness(configFile['mainConfig']['brightness'])
        for key in range(deck.key_count()):
            update_key_image(deck, key, False)
        # Set initial key images.
        # Register callback function for when a key state changes.
        deck.set_key_callback(key_change_callback)

        # Wait until all application threads have terminated (for this example,
        # this is when all deck handles are closed).
        for t in threading.enumerate():
            if t is threading.currentThread():
                continue

            if t.is_alive():
                t.join()
                
def update_key_image(deck, key, state):
    # Determine what icon and label to use on the generated key.
    key_style = get_key_style(deck, key, state)

    # Generate the custom key with the requested image and label.
    image = render_key_image(deck, key_style["icon"])

    # Use a scoped-with on the deck to ensure we're the only thread using it
    # right now.
    with deck:
        # Update requested key with the generated image.
        deck.set_key_image(key, image)
        
def render_key_image(deck, icon_filename):
    # Resize the source image asset to best-fit the dimensions of a single key,
    # leaving a margin at the bottom so that we can draw the key title
    # afterwards.
    icon = Image.open(icon_filename)
    image = PILHelper.create_scaled_image(deck, icon, margins=[0, 0, 20, 0])

    # Load a custom TrueType font and use it to overlay the key index, draw key
    # label onto the image a few pixels from the bottom of the key.
    draw = ImageDraw.Draw(image)
    draw.text((image.width / 2, image.height - 5), text="", anchor="ms", fill="white")

    return PILHelper.to_native_format(deck, image)
     
def get_key_style(deck, key, state):
    try:
        return {
            "name": configFile['ButtonConfig']['Button' + str(key + 1)],
            "icon": os.path.abspath(os.getcwd()) + '/Mt4SDBRIDGE/images/' + configFile['ButtonConfig']['Button' + str(key + 1)]['imagePath'],
        }
    except:
        pass
    
def key_change_callback(deck, key, state):
    if state == True:
        if(configFile['ButtonConfig']['Button' + str(key + 1)]['action'] == "CLOSE"):
            mt4Connector._DWX_MTX_CLOSE_ALL_TRADES_()
        elif(configFile['ButtonConfig']['Button' + str(key + 1)]['action'] == 'BUY'):
            mt4Connector._DWX_MTX_SEND_COMMAND_( _action='OPEN', _type=0,
                _symbol=configFile['mainConfig']['asset'], _price=0.0,
                _SL=50, _TP=50, _comment="Python-to-MT",
                _lots=configFile['ButtonConfig']['Button' + str(key + 1)]['lotSize'], _magic=123456, _ticket=0)
        elif(configFile['ButtonConfig']['Button' + str(key + 1 )]['action'] == 'SELL'):
            mt4Connector._DWX_MTX_SEND_COMMAND_( _action='OPEN', _type=1,
                _symbol=configFile['mainConfig']['asset'], _price=0.0,
                _SL=50, _TP=50, _comment="Python-to-MT",
                _lots=configFile['ButtonConfig']['Button' + str(key + 1)]['lotSize'], _magic=123456, _ticket=0)
        elif(configFile['ButtonConfig']['Button' + str(key + 1)]['action'] == 'CHANGESDPAGE'):
            main()
        elif(configFile['ButtonConfig']['Button' + str(key + 1)]['action'] == 'COMMAND'):
            subprocess.Popen(configFile['ButtonConfig']['Button' + str(key + 1)]['command'],shell=True)
            
    # Check if the key is changing to the pressed state.

def load_config_file():
    configFilePath = str(input("Config file name(on streamDeckConfigs folder): "))
    with open( os.path.abspath(os.getcwd()) + "/Mt4SDBRIDGE/streamDeckConfigs/" + configFilePath, 'r') as f:
        global configFile 
        configFile = json.loads(f.read())

def main():
    os.system('clear')
    load_config_file()
    streamDeskConnection()
    
if __name__ == "__main__":
    main()
