import json

class BuienradarDetailParser:
    
    def __init__(self):
        pass
    
    # Can throw exceptions if errors in parsing
    def parse(self, site, data):
        root = json.loads(data.decode("UTF-8"))  # Get the root element of the json response

        return root
