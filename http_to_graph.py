import requests as req
from matplotlib import pyplot as plt
import datetime as dt
import numpy as np
from os import mkdir

class HttpToGraph:
    def __init__(self, api_url):
        self.api_url = api_url
        self.times=[]
        self.times_formatted=[]
        try:
            mkdir("exports")
        except FileExistsError:
            pass

    def get_json(self):


        r = req.get(f'{self.api_url}')

        raw_json = r.json()["energyPrice"]["values"]


        return raw_json



    def get_today_json(self):
        raw_json=self.get_json()
        today_json = []

        for entry in raw_json:
            if str(entry["dateTimeFrom"][:10]) == str(dt.date.today()):
                today_json.append(entry)

        return today_json
    def today_to_graph(self):
        today_json=self.get_today_json()
        date = today_json[0]["dateTimeFrom"][:10]
        y_data = []
        date_formatted = date[8:10]+'.'+date[5:7]+'.'+date[:4]
        filename = date[8:10]+'-'+date[5:7]+'-'+date[:4]+'.pdf'
        if not self.times:
            for entry in today_json:
                if entry["dateTimeFrom"][14:16]=='15':
                    self.times.append(entry["dateTimeFrom"][11:13] + '.'+'25')
                elif entry["dateTimeFrom"][14:16]=='30':
                    self.times.append(entry["dateTimeFrom"][11:13] + '.'+'50')
                elif entry["dateTimeFrom"][14:16]=='45':
                    self.times.append(entry["dateTimeFrom"][11:13] + '.'+'75')
                else:
                    self.times.append(entry["dateTimeFrom"][11:13] + '.'+'00')

            self.times_formatted=np.array(self.times, dtype=float)

        for entry in today_json:
            y_data.append(entry['value'])


        x_data = self.times_formatted+0.125
        fig, ax = plt.subplots()
        max_today=max(y_data)
        # for future daily average:
        # avg_today=np.average((y_data))
        ax.label = date_formatted
        ax.bar(x_data,y_data,width=0.25)
        plt.grid(axis=('both'))
        plt.title(f'{date}')
        plt.tight_layout()


        ax.set(xlim=(-0.5, 24.5), xticks=(range(0,25)), ylim = (0,max_today+10),yticks = np.arange(0,max_today+10,5))
        plt.savefig(f'exports/{filename}', dpi=300, transparent=True)

        return True

SmartEnergy = HttpToGraph('https://apis.smartenergy.at/tariffs/v1/Tariffs/smartTIMES/prices')
#print(SmartEnergy.get_json())
#print(SmartEnergy.get_today_json())
print(SmartEnergy.today_to_graph())

