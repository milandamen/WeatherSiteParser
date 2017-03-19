import urllib.request

class Site:
    def __init__(self, config):
        if not "url" in config:
            print("config.json is invalid. Site does not have a \"url\" property.")
            exit(1)
        if not "type" in config:
            print("config.json is invalid. Site %s does not have a \"type\" property." % config["url"])
            
        self.url = config["url"]
        self.type = config["type"]
    
    def refresh(self):
        try:
            with urllib.request.urlopen(self.url) as response:
                return response.read()
        except urllib.error.URLError as e:
            return False
        