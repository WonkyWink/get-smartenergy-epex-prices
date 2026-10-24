import requests
from matplotlib import pyplot as plt


def get_values():
    request = requests.get("https://apis.smartenergy.at/tariffs/v1/Tariffs/smartTIMES/prices")
    request.
    raw_json = request.json()
    values=raw_json[0:int(len(raw_json) / 2):4]

    print(values)
    #for entry in values:
     #   print(entry)

get_values()
'''
x_axis = []
for x in range(0,24):
    x_axis.append(x)
print(x_axis)
y_axis = []
for y in range(-20,100,5):
    y_axis.append(y)
print(len(y_axis))
print(y_axis)


#y_axis = range(-10,0,10,20,30,40,50,60,70,80,90,110)
#plt.plot(x_axis, [-10,0,10,20,30,40,50,60,70,80,90,110], marker='o', linestyle='--', color='b')

plt.plot(x_axis, y_axis)
plt.show()
plt.title("Sample Plot")
#plt.savefig("plot.pdf", format="pdf")

# Show the plot
'''