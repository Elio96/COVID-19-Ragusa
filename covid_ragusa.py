import pandas as pd
import ssl
import json
import numpy as np
import matplotlib.pyplot as plt

import Setup
import bot

ssl._create_default_https_context = ssl._create_unverified_context

setup = Setup.Setup()
token = setup.get_token()
channel = setup.get_channel()

df = pd.read_csv('https://query.data.world/s/ujfelswxlbunuxirtuetaagottcnyt')

df.to_json('dati.json', 'records')


def send_data_ragusa():
    with open('dati.json', 'r') as f:
        res = json.load(f)

    days = []
    results = [[], [], [], []]
    for i in res:
        if i['denominazione_provincia'] == 'Ragusa':
            days.append(i["data"][5:10])
            totale_positivi = i["totale_positivi"]
            nuovi_positivi = i["nuovi_positivi"]
            guariti = i["dimessi_guariti"]
            deceduti = i["deceduti"]
            results[0].append(totale_positivi)
            results[1].append(nuovi_positivi)
            results[2].append(guariti)
            results[3].append(deceduti)

    plt.style.use('ggplot')
    fig = plt.figure("Variazione giornaliera Ragusa e provincia (in 7 giorni)", figsize=(10.0, 7.0))
    labels = days[-7:len(days)]
    totale_positivi = results[0][-7:len(results[0])]
    nuovi_positivi = results[1][-7:len(results[0])]
    guariti = results[2][-7:len(results[1])]
    deceduti = results[3][-7:len(results[2])]
    print(totale_positivi)
    print(nuovi_positivi)
    print(guariti)
    print(deceduti)

    index = np.arange(len(labels))

    ax = fig.add_subplot()
    width = 0.20

    tot_pos = plt.bar(index, totale_positivi, width, color='b')
    nuo_pos = plt.bar(index + width, nuovi_positivi, width, color='r')
    gua = plt.bar(index + width * 2, guariti, width, color='g')
    dec = plt.bar(index + width * 3, deceduti, width, color='k')

    plt.xticks(index, labels, fontsize=12, rotation=30)

    plt.title("COVID-19 Ragusa e provincia (in 7 giorni)")
    plt.xlabel("Giorno")
    plt.ylabel("Casi")
    plt.legend((tot_pos, nuo_pos, gua, dec), ("Totale Positivi", "Nuovi Positivi", "Totale Guariti", "Totale Deceduti"))

    def autolabel(rects):
        for rect in rects:
            h = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2., h, '%d' % int(h),
                    ha='center', va='bottom')

    autolabel(tot_pos)
    autolabel(nuo_pos)
    autolabel(gua)
    autolabel(dec)
    plt.savefig("COVID-19_Ragusa.png")

    nuovi_guariti = guariti[-1] - guariti[-2]
    nuovi_decessi = deceduti[-1] - deceduti[-2]

    def text_to_bot_positivi():
        caption = ""
        if totale_positivi[-1] == totale_positivi[-2]:
            caption = "I positivi sono " + str(totale_positivi[-1]) + " = " + str(totale_positivi[-2]) \
                      + "(tot. positivi di ieri)" + " + " + str(nuovi_positivi[-1]) + "(nuovi positivi)" + " - " + str(
                nuovi_guariti) \
                      + "(nuovi guariti)" + " - " + str(nuovi_decessi) + "(nuovi decessi)"
            return caption
        elif totale_positivi[-1] < totale_positivi[-2]:
            caption = "I nuovi positivi sono " + str(totale_positivi[-1]) + " = " + str(totale_positivi[-2]) \
                      + "(tot. positivi di ieri)" + " + " + str(nuovi_positivi[-1]) + "(nuovi positivi)" + " - " + str(
                nuovi_guariti) \
                      + "(nuovi guariti)" + " - " + str(nuovi_decessi) + "(nuovi decessi)"
            return caption
        else:
            caption = "I nuovi positivi sono " + str(totale_positivi[-1]) + " = " + str(totale_positivi[-2]) \
                      + "(tot. positivi di ieri)" + " + " + str(nuovi_positivi[-1]) + "(nuovi positivi)" + " - " + str(
                nuovi_guariti) \
                      + "(nuovi guariti)" + " - " + str(nuovi_decessi) + "(nuovi decessi)"
            return caption

    caption = text_to_bot_positivi()
    bot.sendPhoto(token, channel, caption)
    plt.show()


schedule.every().day.at("12:21").do(send_data_ragusa())
while True:
    schedule.run_pending()
    time.sleep(60)
