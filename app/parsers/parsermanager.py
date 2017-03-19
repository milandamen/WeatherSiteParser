from app.parsers.weerplazadetailparser import WeerplazaDetailParser

class ParserManager:
    def __init__(self):
        self.parsers = {}
        
        self.parsers["weerplaza-detail"] = WeerplazaDetailParser()
        
    def parse(self, site, data):
        if site.type not in self.parsers:
            print("No parser found for type " + site.type)
            return False
        
        try:
            return self.parsers[site.type].parse(site, data)
        except Exception as e:
            print(e)
            print("Could not parse site " + site.url)
            return False