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
        self.interval_percent = round(self.interval * 1.66)

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


  #  helping
    def annotate_axes(fig):
        pass


    def make_arrays(self):
        interval=self.interval_percent
        x_marker_array = np.arange(0.00, 24.00, interval)

        y_marker_array_1 =[]
        y_marker_array_2 =[]


        y_data_array_1 = []
        y_data_array_2 = []

        x_data_array_1 =np.arange(0.00, 24.00, interval*0.01)
        x_data_array_2 =np.arange(0.00, 24.00, interval*0.01)

        y_sum_1 = 0
        y_avg_1 = 0
        y_min_1 = 0
        y_max_1 = 0

        y_sum_2 = 0
        y_avg_2 = 0
        y_min_2 = 0
        y_max_2 = 0



        for entry in self.all_values:
            if entry['dateTimeFrom'][8:10] == self.first_date[8:10]:
                y_data_array_1.append(entry['value'])
                y_sum_1 +=entry['value']
                if not y_min_1 and y_max_1:
                    y_min_1, y_max_1 = entry['value'],entry['value']
                else:
                    if entry['value'] < y_min_1: y_min_1 = entry['value']
                    if entry['value'] > y_max_1: y_max_1 = entry['value']
                    else: pass

            elif entry['dateTimeFrom'][8:10] == self.last_date[8:10]:
                y_data_array_2.append(entry['value'])

                y_sum_2 +=entry['value']
                if not y_min_2 and y_max_2:
                    y_min_2, y_max_2 = entry['value'],entry['value']
                else:
                    if entry['value'] < y_min_2: y_min_2 = entry['value']
                    if entry['value'] > y_max_2: y_max_2 = entry['value']
                    else: pass
        y_avg_1 =y_sum_1/len(y_data_array_1)
        y_axis_range_1 = (y_max_1+1000) - (y_min_1+1000)
        y_axis_range_2 = (y_max_2 + 1000)-(y_min_2 + 1000)
        if y_sum_2 != 0:
            y_avg_2 =y_sum_2/len(y_data_array_2)

        return (x_marker_array,
                y_data_array_1,
                y_data_array_2,
                x_data_array_1,
                x_data_array_2,
                y_sum_1,
                y_avg_1,
                y_min_1,
                y_max_1,
                y_sum_2,
                y_avg_2,
                y_min_2,
                y_max_2,
                y_axis_range_1,
                y_axis_range_2
                )

    # def calculate_sum_avg(self):


    @property
    def plot(self):
        GridSpec(2,1)


        x_marker_array, y_data_array_1,y_data_array_2,x_data_array_1,x_data_array_2,y_axis_range_1,y_axis_range_2,y_sum_1,y_avg_1,y_min_1,y_max_1,y_sum_2,y_avg_2,y_min_2,y_max_2 = self.make_arrays()
        '''print(x_marker_array,
              y_data_array_1,
              y_data_array_2,
              x_data_array_1,
              x_data_array_2,
              y_axis_range_1,
              y_axis_range_2,
              y_sum_1,
              y_avg_1,
              y_min_1,
              y_max_1,
              y_sum_2,
              y_avg_2,
              y_min_2,
              y_max_2)
        '''



        # for entry in self.all_values:
        #     if entry["dateTimeFrom"][14:16] == '15':
        #         self.times.append(entry["dateTimeFrom"][11:13] + '.' + '25')
        #     elif entry["dateTimeFrom"][14:16] == '30':
        #         self.times.append(entry["dateTimeFrom"][11:13] + '.' + '50')
        #     elif entry["dateTimeFrom"][14:16] == '45':
        #         self.times.append(entry["dateTimeFrom"][11:13] + '.' + '75')
        #     else:
        #         self.times.append(entry["dateTimeFrom"][11:13] + '.' + '00')
        #self.times_formatted = np.array(self.times, dtype=float)
        today_date=str(self.today_date)
        date_formatted = today_date[8:10]+'-'+today_date[5:7]+'-'+today_date[:4]
        filename = date_formatted
        print(date_formatted)




        fig, axs = plt.subplots(2)
        plt.tight_layout()
        axs[0].plot(x_data_array_1,y_data_array_1)
        if y_data_array_2: axs[1].plot(x_data_array_2,y_data_array_2)

        bottom_border_1 = ((round(y_min_1) // 10) * 10) +5
        bottom_border_2 = ((round(y_min_2) // 10) * 10) +5
        top_border_1 = ((round(y_min_1) // 10) * 10) - 5
        top_border_2 = ((round(y_min_2) // 10) * 10) - 5
        axs[0].bar(x_data_array_1, y_data_array_1, width=0.25)


        axs[0].set(xlim=(-0.5, 24.5), xticks=(x_marker_array), ylim=(bottom_border_1, top_border_1),
               yticks=np.arange(bottom_border_1, top_border_1, 5))
        if y_data_array_2:
            axs[1].set(xlim=(-0.5, 24.5), xticks=(x_marker_array), ylim=(bottom_border_2, top_border_2),
                   yticks=np.arange(bottom_border_2, top_border_2, 5))
            axs[1].bar(x_data_array_2, y_data_array_2, width=0.25)

        plt.savefig(f'exports/{filename}', dpi=300, transparent=True)

        plt.show()

#https://matplotlib.org/stable/gallery/subplots_axes_and_figures/subplots_demo.html


        return True

    @property
    def price(self, date='today', time='now'):

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



    def __str__(self):
        return (
            f'{self.interval_percent*0.01},\n'
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
            # #   f'{self.isodate},\n '
            # #  f'{self.isodate+dt.timedelta(days=1)},\n '
            # f'{self.first_date},\n'
            # f'{dt.timedelta(days=1)},\n '
            # f'{self.json_raw},\n '
            #
            #

        )


Smartcontrol = ApiCall("https://apis.smartenergy.at/tariffs/v1/Tariffs/smartCONTROL/prices")
print(Smartcontrol)
#print(Smartcontrol.price)
print(Smartcontrol.plot)