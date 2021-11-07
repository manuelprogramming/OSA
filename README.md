## OSA-Remote-Control-System ORCS
This is a system to control the Optical Spectrum Analyzer MS9740B by Anritsu with a remote computer

## Motivation
This is a work related student Project at HOT – Hannoversches Zentrum für Optische Technologien. 


## Tech/framework used
Tech:<br>
-python 3.9, <br> 
-pip 21.1.2, <br>
Frameworks: <br>
-PyVisa 1.11.3, <br>
-numpy 1.19.5, <br>
-pandas 1.2.2, <br>
-matplotlib 3.3.4 <br>


## Features
Its a plugin based remote control system made as console application. For retrieving, saving data, plotting and analyzing optical data.

## Installation
In order for the system to work you have to create a visa_search_term.json file in the bin folder containing a single line:
{"visa_search_term": "Example-Visa-Search-Term"} <br>
For more information how to connect the MS9740B check the [Remote Operation Control Manuel](https://dl.cdn-anritsu.com/en-au/test-measurement/files/Manuals/Operation-Manual/MS9740B/MS9740B_Remote_Operation_Manual_e_2_0.pdf)


## How to use?
For using it you have to change the IP Adress of the MS9740B in settings.json then run the main.py file. If connected you can control the MS9740B with the commands written in the program. The commands for the different tools can be found in data.json. Also new saving folder need to be created.


## License

MIT © Emanuel Pegler
