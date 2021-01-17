"""
download the history of uvxy from yahoo.

Construct a 20 day moving average from the closing prices.

Calculate the distance of the close from the moving average stated as a percentage.

indicator :   (close-20DMA)/close

if the indicator rises above 10%, then sell
If the indicator decline below 0% then buy
"""
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import numpy

#download the history of uvxy from yahoo.
#last index is most recent
def download_history(url):
    session = HTMLSession().get(url)
    page = BeautifulSoup(session.text, features='lxml')
    data = page.find_all("tr", class_="BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)")

    all_close = []
    for i in data:

        entries = i.find_all("td")
        try:
            #4 is close
            all_close.append(float(entries[4].text))
        except:
            pass

    #flip the array so the last index is the most recent
    return all_close[::-1]

#construct 20 day MDA
def get_mda(history):

        percentages = []
        for i in range(20, len(history)):
            mda = []
            for j in range(i - 20, i):
                if history[j] != None:
                    mda.append(history[j])

            mda_average = numpy.average(mda)

            percentage = calculate_percentage(history[i], mda_average)
            percentages.append(percentage)

        return percentages


#Calculate the distance of the close from the moving average stated as a percentage.
#indicator :   (close-20DMA)/close
def calculate_percentage(close, mda):
    return (float(close - mda) / float(close)) * 100


def send_email():
    pass

#if the indicator rises above 10%, then sell
#If the indicator decline below 0% then buy
if __name__ == '__main__':
    url = "https://finance.yahoo.com/quote/UVXY/history?p=UVXY"
    history = download_history(url)
    print(history)
    percentages = get_mda(history)

    for i in percentages:
        print(i)
        if i > 10.0:
            print("sell")
        elif i < 0:
            print("buy")