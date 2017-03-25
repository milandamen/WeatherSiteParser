from app.parsers.weerplazadetailparser import WeerplazaDetailParser
from app.parsers.buienradardetailparser import BuienradarDetailParser

class ParserManager:
    def __init__(self):
        self.parsers = {}
        
        self.parsers["weerplaza-detail"] = WeerplazaDetailParser()
        self.parsers["buienradar-detail"] = BuienradarDetailParser()
        
    def parse(self, site, data):
        print("Parsing " + site.url)
        
        if site.type not in self.parsers:
            print("No parser found for type " + site.type)
            return False
        
        try:
            result = self.parsers[site.type].parse(site, data)
            result["type"] = site.type
            result["url"] = site.url
            return result
        except Exception as e:
            print(e)
            print("Could not parse site " + site.url)
            return False