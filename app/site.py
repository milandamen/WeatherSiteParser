import json
import urllib.request

class Site:
    def __init__(self, config):
        if not "url" in config:
            print("config.json is invalid. Site does not have a \"url\" property.")
            exit(1)
        if not "type" in config:
            print("config.json is invalid. Site %s does not have a \"type\" property." % config["url"])
        if not "filePath" in config:
            print("config.json is invalid. Site %s does not have a \"filePath\" property." % config["url"])
            
        self.url = config["url"]
        self.type = config["type"]
        self.filePath = config["filePath"]
    
    def refresh(self):
        try:
            print("Grabbing " + self.url)
            with urllib.request.urlopen(self.url) as response:
                return response.read()
        except urllib.error.URLError as e:
            return False
    
    def saveResult(self, result):
        print("Saving result for site " + self.url)
        
        try:
            f = open(self.filePath, "w")
            f.write(json.dumps(result, indent=2))
            f.close()
        except Exception as e:
            print(e)
            print("Could not save result for site " + self.url)