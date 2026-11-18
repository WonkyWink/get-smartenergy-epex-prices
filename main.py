import datetime as dt
import requests as rq
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np

class ApiCall:
    def __init__(self, url: str):
        self.url = url
        self.today_date = dt.date.today()
        self.now_time = dt.datetime.today().strftime("%H:%M:%S")
        self.refresh_time = "17:00:00"

        if self.now_time <= self.refresh_time:
            self.anchor_date = self.today_date  # "today"
        else:
            self.anchor_date = self.today_date + dt.timedelta(days=1)  # "tomorrow"
        self.response = rq.get(url)
        if self.response.status_code != 200: raise ValueError("Bad API response")
        self.json_raw = self.response.json()
        #how long is the price valid in minutes (15,60,..)
        self.interval = self.json_raw["energyPrice"]["interval"]

        # raw values including price/currency per entry
        self.all_values = self.json_raw["energyPrice"]["values"]
        # data DateTime
        self.data_first_datetime = self.all_values[0]["dateTimeFrom"]
        self.data_last_datetime = self.all_values[-1]["dateTimeFrom"]
        # data Timezones
        self.tz_first_datetime = f'UTC{self.data_first_datetime[-6:]}'
        self.tz_last_datetime = f'UTC{self.data_last_datetime[-6:]}'
        #
        self.first_date = f'{self.data_first_datetime[:10]}'
        self.last_date = f'{self.data_last_datetime[:10]}'
        # self.all_values=self.json_raw["energyPrice"]["values"]
        if self.first_date == self.last_date:
            self.timespan = 1  # 1 day
        else:
            if self.first_date + dt.timedelta(days=1) == self.last_date:
                self.timespan = 2  # 2 days
            else:
                raise Exception("Faulty date/time")


    @property
    def get_price(self, date='today', time='now'):

        if date == 'today' and time == 'now':
            time_from_hour = str(self.now_time[:2])

            if self.interval == 15:

                if  int(self.now_time[3:5]) < 15:
                    time_from_min = "00"
                elif int(self.now_time[3:5]) < 30:
                    time_from_min = "15"
                elif int(self.now_time[3:5]) < 45:
                    time_from_min = "30"
                elif int(self.now_time[3:5]) <60:
                    time_from_min = "45"
                else:
                    raise SyntaxError ("invalid minutes value")
                print(time_from_hour,time_from_min)

                for entry in self.all_values:
                    #print(entry["dateTimeFrom"][14:16])
                    if entry["dateTimeFrom"][11:13] == time_from_hour and entry["dateTimeFrom"][14:16] == time_from_min:
                        return  entry["value"]
                    else:
                        continue
            return False
        else:
            print ('not implemented yet')

  #  helping
    def annotate_axes(fig):
        pass




    @property
    def get_plot(self):
        GridSpec(2,1)
        xa = 1,2,3
        ya = 0,1,3
        xb = np.arange(0,24,0.25)
        yb = np.arange(0,24,0.25)
        fig, axs = plt.subplots(2)
        fig.suptitle('Vertically stacked subplots')
        axs[0].plot(xa, ya)
        axs[1].plot(xb, yb)


#        plt.tight_layout()
        plt.plot(xa,ya)
        fig, axs = plt.subplots(2)
        fig.suptitle('Vertically stacked subplots')
        axs[0].plot(xa, ya)
        axs[1].plot(xb, yb)
        plt.show()

#https://matplotlib.org/stable/gallery/subplots_axes_and_figures/subplots_demo.html


        return True


    def __str__(self):
        return (

            # f'{self.url},\n '
            # f'{self.today_date},\n '
            # f'{self.now_time},\n '
            # f'{self.refresh_time},\n '
            # f'{self.response},\n '
            # f'{type(self.response)},\n '
            # f'{self.anchor_date},\n '
            #
            #
            # f'{self.interval},\n '
            # f'{self.data_first_datetime},\n '
            # # f'{self.data_first_date},\n '
            # # f'{self.data_last_datetime},\n '
            # # f'{self.data_last_date},\n '
            #
            # f'{self.data_first_datetime},\n '
            # f'{self.tz_first_datetime},\n '
            # f'{self.tz_last_datetime},\n '
            # # f'{(self.data_first_datetime+dt.timedelta(days=1))[:10]},\n '
            # f'{self.first_date},\n '
            # f'{self.last_date},\n '
            # f'{'xxxxx'},\n '
            # f'{'xxxxx'},\n '
            # f'{'xxxxx'},\n '
            # #   f'{self.isodate},\n '
            # #  f'{self.isodate+dt.timedelta(days=1)},\n '
            # f'{self.first_date},\n'
            # f'{dt.timedelta(days=1)},\n '
            # f'{self.json_raw},\n '
            #
            #

        )


Smartcontrol = ApiCall("https://apis.smartenergy.at/tariffs/v1/Tariffs/smartCONTROL/prices")
#print(Smartcontrol)
print(Smartcontrol.get_price)
print(Smartcontrol.get_plot)