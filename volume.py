import requests
from bs4 import BeautifulSoup
import matplotlib
import matplotlib.pyplot as plt
import numpy as np




url = 'https://finance.yahoo.com/most-active/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')



p = input('Enter the percentage to screen the volume as a decimal: ')
percent = float(p)


tickers = []
curr_vol = []
avg_vol = []

new_tickers = []
new_vol = []
their_avg = []


for tr in soup.find_all('tr')[1:]:

    tds = tr.find_all('td')
    tickers.append(str(tds[0].text))

    st =  tds[5].text
    st = st[:-1]
    curr_vol.append(float(st))

    st2 =  tds[6].text
    st2 = st2[:-1] 
    avg_vol.append(float(st2))





# This is the algorithm that will check which of the stock's volume is above its
# average by the given percentage
def check_vol():
    
    i = 0
    while i < len(avg_vol) :
        if curr_vol[i] > ((avg_vol[i] * percent) + avg_vol[i]):
            new_tickers.append(tickers[i])
            new_vol.append(curr_vol[i])
            their_avg.append(avg_vol[i])
        i = i + 1


check_vol()





# matplotlib creation

x = np.arange(len(new_tickers))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, new_vol, width, label='current volume')
rects2 = ax.bar(x + width/2, their_avg, width, label='average volume')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Volume (millions)')
ax.set_title('Current Volume vs Average Volume')
ax.set_xticks(x)
ax.set_xticklabels(new_tickers)
ax.legend()

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)

fig.tight_layout()

plt.show()