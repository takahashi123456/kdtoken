from .models import SampleModel, HorseModel                       # モデル呼出
from datetime import datetime, date

from bs4 import BeautifulSoup
from googletrans import Translator
from selenium import webdriver
import chromedriver_binary
import requests
from concurrent import futures

import pandas as pd
import numpy as np
import os
import glob
import re
import time

class ScrapingBase():
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome('chromedriver',options=options)
        self.driver.implicitly_wait(10)

        # 設定
        self.year =2022
        self.keibajyou = 3
        self.kai = 3
        self.nichime = 4
        self.race = 0


        self.keibajyou_list = ['01','02','03','04','05','06','07','08','09','10']
        self.kai_list = ['01','02','03','04','05','06']
        self.nichime_list = ['01','02','03','04','05','06','07','08','09','10','11','12']
        self.race_list = ['01','02','03','04','05','06','07','08','09','10','11','12']


class RaceScraping(ScrapingBase):
    def race_data_scraping(self): # スクレイピング処理
        print('start')  # 動作確認用

        url = 'https://race.netkeiba.com/race/shutuba.html?race_id=' +  str(self.year) + str(self.keibajyou_list[self.keibajyou]) + str(self.kai_list[self.kai]) + str(self.nichime_list[self.nichime]) + str(self.race_list[self.race])
        
        soup = BeautifulSoup(requests.get(url).content, 'lxml')
        span =  soup.select_one('#page > div.RaceColumn01 > div > div.RaceMainColumn > div.RaceList_NameBox > div.RaceList_Item02 > div.RaceData01').get_text().strip()
        self.race_data = [[j.strip() for j in i.split(':', 1)] for i in span.split('/')]

        self.driver.get(url)

        self.html = self.driver.page_source.encode('utf-8')

    def data_shape(self): # データ整形

        def change_en(value_data):
            return  translator.translate(value_data).text

        def age(value_data):
            return int(value_data[1:])

        def gender(value_data):
            if value_data[:1] == '牡':
                return 'male'
            elif value_data[:1] == '牝':
                return 'female'
            else :
                return 'gelding'

        def horse_weight(value_data):
            return int(value_data[:value_data.find('(')])
            
        def weight_cycling(value_data):
            return int(str(value_data[value_data.find('('):]).replace("(","").replace(")",""))

        def trainer(value_data):
            if value_data[:2] == '栗東':
                return str(value_data.replace('栗東', '[東]'))
            elif value_data[:2] == '美浦':
                return str(value_data.replace('美浦', '[西]'))
            else :
                return str('none')

        translator = Translator()
        data_list = pd.DataFrame()

        wether = {'晴':'sunny', '曇':'cloudy','雨': 'rain', '小雨':'light rain', '雪':'snowy', '小雪':'light snowy'}
        track_condition = {'良':'firm', '稍':'good', '重':'soft', '不良':'heavy'}
        racecourse_list = {'01':'Sapporo', '02':'Hakodate', '03':'Fukushima', '04':'Niigata', '05':'Tokyo', '06':'Nakayama', '07':'Chukyo', '08':'Kyoto', '09':'Hanshin', '10':'Kokura'}

        self.race_data_scraping()
        
        data_new = pd.read_html(self.html, encoding='utf-8')[0]

        data_new.columns = [''.join(col) for col in data_new.columns.values]
        data_new = data_new.drop(columns= ['印印', 'お気に入り馬登録', 'お気に入り馬メモ'])
        data_new = data_new.set_axis(['枠番', '馬番', '馬名', '性齢', '斤量', '騎手', '調教師', '馬体重', '単勝', '人気'], axis=1)
        data_new = data_new.reindex(['枠番', '馬番', '馬名', '性齢', '斤量', '騎手', '単勝', '人気', '馬体重', '調教師'], axis=1)

        data_new['horse_name'] = data_new['馬名'].apply(change_en)
        data_new['jockey'] = data_new['騎手'].apply(change_en)
        data_new['調教師'] = data_new['調教師'].apply(trainer)
        data_new['trainer'] = data_new['調教師'].apply(change_en)
        data_new['age'] = data_new['性齢'].apply(age)
        data_new['gender'] = data_new['性齢'].apply(gender)
        data_new['horse_weight'] = data_new['馬体重'].apply(horse_weight)
        data_new['weight_cycling'] = data_new['馬体重'].apply(weight_cycling)
        data_new['racecourse'] = str(racecourse_list[str(self.keibajyou_list[self.keibajyou])])
        data_new['turn'] = 'clockwise' if re.findall('(?<=\().+?(?=\))', str(self.race_data[1]))[0]  == '右' else 'anticlockwise'
        data_new['circumference'] = int(re.sub(r"\D", "", self.race_data[1][0]))
        data_new['wether'] = wether[self.race_data[2][1]]
        data_new['track_surface'] = 'grass' if self.race_data[1][0][:1]  == '芝' else 'dirt'
        data_new['track_condition'] = track_condition[self.race_data[3][1]]
        data_new['race_id'] = str(self.year) + str(self.keibajyou_list[self.keibajyou]) + str(self.kai_list[self.kai]) + str(self.nichime_list[self.nichime]) + str(self.race_list[self.race])
        data_new = data_new.rename(columns={'枠番':'bracket_number', '馬番':'horse_number', '斤量':'penalty', '単勝':'odds', '人気':'favorite'})
        data_new[['penalty', 'favorite']] = data_new[['penalty', 'favorite']].astype('int')
        data_new[['odds']] = data_new[['odds']].astype('float')
        data_new = data_new.drop(columns= ['馬名', '騎手', '調教師', '性齢', '馬体重'])

        data_list = pd.concat([data_list, data_new],ignore_index=True)

        data_list = data_list.reindex(columns=[
                                        'race_id',
                                        'bracket_number',
                                        'horse_number',
                                        'horse_name',
                                        'gender',
                                        'age',
                                        'penalty',
                                        'jockey',
                                        'trainer',
                                        'horse_weight',
                                        'weight_cycling',
                                        'odds',
                                        'favorite',
                                        'racecourse',
                                        'track_surface',
                                        'circumference',
                                        'turn',
                                        'wether',
                                        'track_condition'
                                        ])

        # data_list.to_csv('[PATHを指定]' + str(self.year) + str(self.keibajyou_list[self.keibajyou]) + str(self.kai_list[self.kai]) + str(self.nichime_list[self.nichime]) + str(self.race_list[race]) + '.csv')
        # print(data_list)
        return data_list
