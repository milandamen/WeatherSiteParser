#!python3

# TODO requirement: sudo pip3 install lxml
# TODO requirement: sudo pip3 install cssselect

from app.config import Config
from app.parsers.parsermanager import ParserManager

config = Config()
parserManager = ParserManager()

for site in config.sites:
    # Fetch the site page from the internet
    response = site.refresh()
    if response == False:
        print("Site %s could not be reached." % site.url)
        continue
    
    # Parse the response
    result = parserManager.parse(site, response)    # TODO add try/catch
    if result == False:
        continue