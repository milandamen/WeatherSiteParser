# WeatherSiteParser
Grab weather data from weather sites

## Requirements
* Python 3
* Python module lxml (`sudo pip3 install lxml`)
* Python module cssselect (`sudo pip3 install cssselect`)

## Usage
1. Open a terminal window and go to the directory you've downloaded this program in
2. Run `python3 main.py`
3. The output gets put in the folder specified in the config.json

## Configuration
Check the config.json file for examples.

### Specification
`url` is the URL being grabbed by the program  
`type` is the parser used by the program. Parsers are listed in app/parsermanager.py  
`filePath` is the path to the file that the outputs gets saved as

## Supported sites
### Weerplaza
Detail page for Weerplaza.  
Example url: http://www.weerplaza.nl/nederland/amsterdam/5575/  
Type: `weerplaza-detail`

### Buienradar API
API page for Buienradar.  
Example url: http://api.buienradar.nl/data/forecast/1.1/all/2759794  
Type: `buienradar-detail`

The last number is the ID of the city. You can get this number by searching for the city and copying the ID from the address bar.
