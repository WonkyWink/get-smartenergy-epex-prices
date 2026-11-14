import requests as req
from matplotlib import pyplot as plt
import datetime as dt
import numpy as np
from os import mkdir

days = ["Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"]

class HttpToGraph:
    def __init__(self, api_url):
        self.api_url = api_url
        self.times=[]
        self.times_formatted=[]
        try:
            mkdir("exports")
        except FileExistsError:
            pass
#get full json
    def get_json(self):
        r = req.get(f'{self.api_url}')
        raw_json = r.json()["energyPrice"]["values"]
        return raw_json
#filter for today
    def get_today_json(self):
        raw_json=self.get_json()
        result = []
        for entry in raw_json:
            if str(entry["dateTimeFrom"][:10]) == str(dt.date.today()):
                result.append(entry)
        return result
    def get_tomorrow_json(self):
        raw_json=self.get_json()
        result = []

        for entry in raw_json:
            if str(entry["dateTimeFrom"][:10]) == str(dt.date.today()+dt.timedelta(days=1)):
                result.append(entry)
        if result: return result
        else: pass
            #raise FileNotFoundError("tomorrow data not present")

    def today_to_graph(self):
        today_json=self.get_today_json()
        date = today_json[0]["dateTimeFrom"][:10]
        weekday_number=dt.datetime.weekday(dt.date.fromisoformat(date))
        weekday_str=days[weekday_number]
        y_data = []
        date_formatted = date[8:10]+'-'+date[5:7]+'-'+date[:4]
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
            y_data.append(entry['value']+2.988)


        x_data = self.times_formatted+0.125
        fig, ax = plt.subplots()
        min_today=min(y_data)
        bottom_border = ((round(min_today)//10)*10) -5
        max_today=max(y_data)
        # for future daily average:
        # avg_today=np.average((y_data))
        ax.label = date_formatted
        ax.bar(x_data,y_data,width=0.25)
        plt.grid(axis='both')
        plt.title(f'{weekday_str},{date}')
        plt.tight_layout()

        ax.set(xlim=(-0.5, 24.5), xticks=(range(0,25)), ylim = (bottom_border,max_today),yticks = np.arange(bottom_border ,max_today+5,5))
        #test the output:
        #print(plt.show())
        plt.savefig(f'exports/{filename}', dpi=300, transparent=True)

        return True

    def tomorrow_to_graph(self):
        today_json = self.get_tomorrow_json()
        if not today_json: return False
        date = today_json[0]["dateTimeFrom"][:10]
        weekday_number=dt.datetime.weekday(dt.date.fromisoformat(date))
        weekday_str=days[weekday_number]
        y_data = []
        date_formatted = date[8:10] + '-' + date[5:7] + '-' + date[:4]
        filename = date[8:10] + '-' + date[5:7] + '-' + date[:4] + '.pdf'
        if not self.times:
            for entry in today_json:
                if entry["dateTimeFrom"][14:16] == '15':
                    self.times.append(entry["dateTimeFrom"][11:13] + '.' + '25')
                elif entry["dateTimeFrom"][14:16] == '30':
                    self.times.append(entry["dateTimeFrom"][11:13] + '.' + '50')
                elif entry["dateTimeFrom"][14:16] == '45':
                    self.times.append(entry["dateTimeFrom"][11:13] + '.' + '75')
                else:
                    self.times.append(entry["dateTimeFrom"][11:13] + '.' + '00')

            self.times_formatted = np.array(self.times, dtype=float)

        for entry in today_json:
            y_data.append(entry['value'] + 2.988)

        x_data = self.times_formatted + 0.125
        fig, ax = plt.subplots()
        min_today = min(y_data)
        bottom_border = ((round(min_today) // 10) * 10) - 5

        max_today = max(y_data)
        # for future daily average:
        # avg_today=np.average((y_data))
        ax.label = date_formatted
        ax.bar(x_data, y_data, width=0.25)
        plt.grid(axis='both')
        plt.title(f'{weekday_str},{date}')
        plt.tight_layout()

        ax.set(xlim=(-0.5, 24.5), xticks=(range(0, 25)), ylim=(bottom_border, max_today),
               yticks=np.arange(bottom_border, max_today + 5, 5))
        #test the output:
        #print(plt.show())

        plt.savefig(f'exports/{filename}', dpi=300, transparent=True)

        return True

SmartEnergy = HttpToGraph('https://apis.smartenergy.at/tariffs/v1/Tariffs/smartCONTROL/prices')
#Remove # to choose day for graph
SmartEnergy.today_to_graph()
SmartEnergy.tomorrow_to_graph()


