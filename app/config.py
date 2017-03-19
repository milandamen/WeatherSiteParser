import json
import os.path

from app.site import Site

class Config:
    
    def __init__(self):
        self.sites = []
        
        f = open('config.json')
        data = json.load(f)
        f.close()
        
        self.savedir = data["savedir"]
        if not self.savedir.endswith("/"):
            self.savedir = self.savedir + "/"
        if not os.path.isdir(self.savedir):
            print("No directory with this name exists: " + self.savedir)
            exit(1)
        
        for site in data["sites"]:
            self.sites.append(Site(site))