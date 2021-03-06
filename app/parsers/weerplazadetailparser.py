import datetime
import re
from lxml.html import fromstring

class WeerplazaDetailParser:
    
    def __init__(self):
        self.weekdays = ["ma", "di", "wo", "do", "vr", "za", "zo"]
    
    # Can throw exceptions if errors in parsing
    def parse(self, site, data):
        self.result = result = {}
        
        root = fromstring(data)                             # Get the root element of the html page
        
        result["dayprediction"] = []
        result["hourprediction"] = []
        
        # Coming 14 days
        tables = (root.cssselect(".forecast-fullday .content")[0]
                      .getchildren()[0]
                      .getchildren()[1]
                      .cssselect("table"))      # <table>
        
        self.parse7Days(tables[0])              # Parse first 7 days
        self.parse7Days(tables[len(tables) - 1])# Parse next 7 days
        
        table = root.cssselect(".forecast-hourly .content table")[0]
        
        self.parse48Hours(table)
        
        return result
    
    # Parse 7 days of the 14 days
    def parse7Days(self, table):
        result = self.result
        startIndex = len(result["dayprediction"])
        
        tbody = table.getchildren()[0]          # <tbody>
        row = tbody.getchildren()[0]            # <tr>          first row
        for td in row.getchildren():            # <td>          each td
            d = {}
            
            # Date
            date = td.attrib["data-day"]        # Format: DDMMYYYY
            date = date[4:] + date[2:4] + date[0:2]  # Format: YYYYMMDD
            d["date"] = date
            
            # Weather rating
            ratingSpan = td.cssselect(".weather-rating")[0]     # <span>
            ratingClasses = ratingSpan.attrib["class"].split(" ")
            for rClass in ratingClasses:
                if rClass.startswith("r-"):
                    d["rating"] = rClass[2:]
            
            if not "rating" in d:
                print("No weather rating found for row")
                
            # Weather icon
            weather = {}
            weatherDiv = td.cssselect(".wx")[0]
            weatherStyle = weatherDiv.attrib["style"]
            #regex: background-image: url\('.+\/(.+).png'\)
            weatherRegex = re.search("background-image: url\('.+\/(.+)@2x.png'\)", weatherStyle)
            weather["id"] = weatherRegex.group(1)       # First capture group
            weather["title"] = weatherDiv.attrib["title"]
            d["weather"] = weather
            
            result["dayprediction"].append(d)
        
        i = startIndex
        row = tbody.getchildren()[1]            # <tr>          second row
        for td in row.getchildren():            # <td>          each td
            d = result["dayprediction"][i]
            
            # Sunchance in %
            sunchanceDiv = td.getchildren()[0]
            d["sunchance"] = sunchanceDiv.text_content().strip(" %")
            i += 1
        
        i = startIndex
        row = tbody.getchildren()[2]            # <tr>          third row
        for td in row.getchildren():            # <td>          each td
            d = result["dayprediction"][i]
            temp = {}
            
            # Max temperature in degrees Celcius
            temp["max"] = td.cssselect("div.red.temp")[0].text.strip()[:-2]
            
            # Min temperature in degrees Celcius
            temp["min"] = td.cssselect("div.blue.temp")[0].text.strip()[:-2]
            
            d["temperature"] = temp
            i += 1
        
        i = startIndex
        row = tbody.getchildren()[3]            # <tr>          fourth row
        for td in row.getchildren():            # <td>          each td
            d = result["dayprediction"][i]
            rain = {}
            
            # Rain chance in %
            rainChanceDiv = td.getchildren()[0]
            rain["chance"] = rainChanceDiv.text_content().strip(" %")
            
            # Rain amount in mm
            rainAmountDiv = td.getchildren()[1]
            rain["amount"] = rainAmountDiv.text.strip(" m")
            
            d["rain"] = rain
            i += 1
        
        i = startIndex
        row = tbody.getchildren()[4]            # <tr>          fifth row
        for td in row.getchildren():            # <td>          each td
            d = result["dayprediction"][i]
            wind = {}
            
            windDescription = td.getchildren()[0].text.split(" ")
            
            # Wind direction
            wind["direction"] = windDescription[0]
            # Wind power
            wind["power"] = windDescription[1]
            
            d["wind"] = wind
            i += 1
    
    # Parse coming 48 hours
    def parse48Hours(self, table):
        result = self.result
        
        tbody = table.getchildren()[0]          # <tbody>
        row = tbody.getchildren()[0]            # <tr>          first row
        for td in row.getchildren():            # <td>          each td
            d = {}
            
            # Date and time
            day = td.getchildren()[0].getchildren()[0].text
            time = td.getchildren()[0].getchildren()[1].text.split(":")
            
            dayIndex = self.weekdays.index(day)
            now = datetime.datetime.today()
            
            # Get the correct datetime for the target day
            destDay = None
            if now.weekday() is dayIndex:
                destDay = now
            elif dayIndex > now.weekday():
                destDay = now + datetime.timedelta(days=(dayIndex - now.weekday()))
            else:
                destDay = now + datetime.timedelta(days=(7 - (now.weekday() - dayIndex)))
            
            destDay = destDay.replace(
                hour = int(time[0]),
                minute = int(time[1])
            )
            
            d["date"] = destDay.strftime("%Y%m%d")
            d["time"] = destDay.strftime("%H%M")
            
            # Weather icon
            weather = {}
            weatherDiv = td.cssselect(".wx")[0]
            weatherStyle = weatherDiv.attrib["style"]
            #regex: background-image: url\('.+\/(.+).png'\)
            weatherRegex = re.search("background-image: url\('.+\/(.+).png'\)", weatherStyle)
            weather["id"] = weatherRegex.group(1)       # First capture group
            d["weather"] = weather
            
            result["hourprediction"].append(d)
        
        i = 0
        row = tbody.getchildren()[1]            # <tr>          second row
        for td in row.getchildren():            # <td>          each td
            d = result["hourprediction"][i]
            temp = {}
            
            # Max temperature in degrees Celcius
            temp["max"] = td.cssselect("div.red.temp")[0].text.strip()[:-2]
            
            d["temperature"] = temp
            i += 1
        
        i = 0
        row = tbody.getchildren()[3]            # <tr>          fourth row
        for td in row.getchildren():            # <td>          each td
            d = result["hourprediction"][i]
            rain = {}
            
            # Rain amount in mm
            rainAmountDiv = td.getchildren()[1]
            rain["amount"] = rainAmountDiv.text.strip(" m")
            
            d["rain"] = rain
            i += 1
        
        i = 0
        row = tbody.getchildren()[5]            # <tr>          sixth row
        for td in row.getchildren():            # <td>          each td
            d = result["hourprediction"][i]
            wind = {}
            
            windDescription = td.getchildren()[0].text.split(" ")
            
            # Wind direction
            wind["direction"] = windDescription[0]
            # Wind power
            wind["power"] = windDescription[1]
            
            d["wind"] = wind
            i += 1
        