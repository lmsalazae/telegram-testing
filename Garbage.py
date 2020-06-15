#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 18:51:45 2020

@author: Miguel Salazar
"""

from telegram.ext import Updater, PrefixHandler
from datetime import datetime, timedelta
import requests
#import re

#import PIL
#from PIL import ImageFont
#from PIL import Image
#from PIL import ImageDraw

import matplotlib.pyplot as plt
#import numpy as np

##Obtencion de datos resumen para comando _info
try:
    contents = requests.get('https://api.covid19api.com/summary').json()
    countries=contents['Countries']
    print('server correct')
except:
    print('server error')

def get_index(a):
    index={}
    for country in countries:
        attached={country['CountryCode']:countries.index(country)}
        index=dict(**index,**attached)
    return index[a]

#print(get_index('CO'))

def get_data(b):
    state=countries[get_index(b)]
    text='Country: '+'\t'+state['Country'] +'\n'+'NewConfirmed: '+'\t'+str(state['NewConfirmed'])+'\n'+'TotalConfirmed: '+'\t'+str(state['TotalConfirmed'])+'\n'+'NewDeaths: '+'\t'+str(state['NewDeaths'])+'\n'+'TotalDeaths: '+'\t'+str(state['TotalDeaths'])+'\n'+'NewRecovered: '+'\t'+str(state['NewRecovered'])+'\n'+'TotalRecovered: '+'\t'+str(state['TotalRecovered'])+'\n'+'Date: '+'\t'+str(datetime.strptime(state['Date'], '%Y-%m-%dT%H:%M:%SZ')-timedelta(hours=5))
    return text

#print(get_data('CO'))

##Generacion de graficas acumuladas
def call_api(a):
    contents = requests.get('https://api.covid19api.com/total/dayone/country/'+a).json()
    table=[]
    for x in range(len(contents)):
        one_to_one=contents[x]
        items=dict({
                    'Code':one_to_one['CountryCode'],
                    'Confirmed':one_to_one['Confirmed'],
                    'Deaths':one_to_one['Deaths'],
                    'Recovered':one_to_one['Recovered'],
                    'Date':datetime.strptime(one_to_one['Date'], '%Y-%m-%dT%H:%M:%SZ')
                   })
        table.append(items)
    print('server correct')
    return table

def get_data_draw(country,status):

    try:
        data=call_api(country)
    except:
        print('server error')
        
    if status=='confirmed':
        confirmed=[]
        for x in range(len(data)):
            confirmed.append(data[x]['Confirmed'])
        return confirmed
        

#get_data_draw('mexico','date')

        
    elif status=='deaths':
        deaths=[]
        for x in range(len(data)):
            deaths.append(data[x]['Deaths'])
        return deaths
        
    elif status=='recovered':
        recovered=[]
        for x in range(len(data)):
            recovered.append(data[x]['Recovered'])
        return recovered
    
    elif status=='date':
        date=[]
        for x in range(len(data)):
            data_aux=data[x]['Date']
            #data_aux=data[x]['Date']-timedelta(hours=5)
            #data_aux=datetime.strftime(data_aux,'%b %d, %Y')
            data_aux=datetime.strftime(data_aux,'%b %d')
            date.append(data_aux)
        return date

def draw_img(b,c): 
    plt.figure(figsize=(8,4))
    vdate=get_data_draw(b,'date')
    lines1=plt.plot(vdate,get_data_draw(b,c))
    plt.setp(lines1, color='r', linewidth=2, marker='.', markersize=15)
    plt.axis([int(len(vdate)-12), int(len(vdate)), None, None])
    plt.xlabel('date')
    plt.ylabel(c)
    plt.title(b.upper()+' - '+c+' at the time: COVID')
    plt.grid()
    url_graph='/home/ubuntu/projectzero/bot0project/image_{}_{}.png'.format(b,c)
    plt.savefig(url_graph, bbox_inches='tight')
    plt.close()
    return url_graph

#draw_img('mexico','confirmed')

##Definicion de funciones finales y comunicacion con Telegram
##Datos resumen
def dataco(bot, update):
    #chat_id = update.message.chat_id
    update.message.reply_text(get_data('CO'))
    
def datamx(bot, update):
    #chat_id = update.message.chat_id
    update.message.reply_text(get_data('MX'))

##Graficas acumuladas 
def co_confirmed(bot, update):
    url_send=draw_img('colombia','confirmed')
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=open(url_send, 'rb'))

def mx_confirmed(bot, update):
    url_send=draw_img('mexico','confirmed')
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=open(url_send, 'rb'))
    
def co_deaths(bot, update):
    url_send=draw_img('colombia','deaths')
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=open(url_send, 'rb'))

def mx_deaths(bot, update):
    url_send=draw_img('mexico','deaths')
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=open(url_send, 'rb'))

def co_recovered(bot, update):
    url_send=draw_img('colombia','recovered')
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=open(url_send, 'rb'))
    
def mx_recovered(bot, update):
    url_send=draw_img('mexico','recovered')
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=open(url_send, 'rb'))

def helptext(bot, update):
    #chat_id = update.message.chat_id
    update.message.reply_text('Comands:\n\nGraphics:\n/co_confirmed : confirmed cases for colombia\n/mx_confirmed : confirmed cases for mexico\n/co_deaths : deaths cases for colombia\n/mx_deaths : deaths cases for mexico\n/co_recovered : recovered cases for colombia\n/mx_recovered : recovered cases for mexico\n\nInfo:\n/co_info : summary of covid disease in colombia\n/mx_info : summary of covid disease in mexico\n/help : this info')
    
#def test(bot, update):
#    #url_send=draw_img('mexico','confirmed')
#    #url_send=get_data_draw('mexico','date')
#    chat_id = update.message.chat_id
#    update.message.reply_text('test text')


def main():
    updater = Updater('')
    dp = updater.dispatcher
    dp.add_handler(PrefixHandler(['!', '#', '.', '/'], 'co_confirmed', co_confirmed))
    dp.add_handler(PrefixHandler(['!', '#', '.', '/'], 'mx_confirmed', mx_confirmed))
    dp.add_handler(PrefixHandler(['!', '#', '.', '/'], 'co_deaths', co_deaths))
    dp.add_handler(PrefixHandler(['!', '#', '.', '/'], 'mx_deaths', mx_deaths))
    dp.add_handler(PrefixHandler(['!', '#', '.', '/'], 'co_recovered', co_recovered))
    dp.add_handler(PrefixHandler(['!', '#', '.', '/'], 'mx_recovered', mx_recovered))
    dp.add_handler(PrefixHandler(['!', '#', '.', '/'], 'mx_info', datamx))
    dp.add_handler(PrefixHandler(['!', '#', '.', '/'], 'co_info', dataco))
    dp.add_handler(PrefixHandler(['!', '#', '.', '/'], 'help', helptext))
    #dp.add_handler(PrefixHandler('!', 'test', test))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()