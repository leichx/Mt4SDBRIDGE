# Python MT4 Stream deck bridge

You have to install python > 3.0 and the package manager pip

## Project Status:
Currently the following StreamDeck product variants are supported:
* StreamDeck Original (both V1 and V2 hardware variants)
* StreamDeck Mini
* StreamDeck XL


## Package Installation:

Install Python library's via pip:

```
pip install streamdeck zmq 

```
Go to folder ```MT4INCLUDES``` and copy the content of ```ExperAdvisor``` in your expert advisors in MT4, copy the content of ```Include``` folder in MT4 Includes folder and copy the content of ```Library``` on your MT4 Library folder.

The folder "streamDeckConfigs" folder contains .json files with the configuration of your stream deck keys, you have to has as many buttons as your stream deck has in the json file. You can configure the actions ``` "BUY", "SELL", "CLOSE", "CHANGESDPAGE","COMMAND" ```, see the .json file to get an idea.

The folder /images/ includes several images for BUY/SELL/CLOSE and CHANGEPAGE

The main folder of the scripts should be named ```Mt4SDBRIDGE```

## Execution:

Go to your expert advisors in MT4 and execute ```Server```.
<br>
Execute   ``` python3 MT4_STREAMDECK_BRIDGE.py ``` in your command line (with stream deck connected)
Input your desired configfile full name (include .json)
