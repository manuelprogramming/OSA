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
In order for the system to work you have to create a visa_search_term.json file in the bin folder containing a single line:<br>
{"visa_search_term": "Example-Visa-Search-Term"} <br>
For more information how to connect the MS9740B check the [Remote Operation Control Manuel](https://dl.cdn-anritsu.com/en-au/test-measurement/files/Manuals/Operation-Manual/MS9740B/MS9740B_Remote_Operation_Manual_e_2_0.pdf) <br>
Also a folder for saving the data needs to be created. The folder must be created in the same folder as the project. The name can be found and changed in the settings.json file.



## How to use?
If connected you can control the MS9740B with the commands and have some additional features unrelated to the MS9740B like saving, analyzing and plotting. The tools available for ORCS will be printed on starting the system. For more information what the commands exactly do you can read the docstrings within the different tools in the plugin folder.


## License

MIT © 2021 Emanuel Pegler

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
