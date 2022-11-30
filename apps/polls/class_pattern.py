import datetime
import os
import glob
import re
import time

from googletrans import Translator
from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_binary
import requests
import pandas as pd
import numpy as np

class main:
    def __init__(self):
        pass

    def day_races_get(self):
        DayRaces().data_shaping()

    def one_race_get(self, id=None):
        OneRace(id).data_shaping()


class Base:

    def scraping_base(self):
        # seleniumの設定
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome('chromedriver',options=options)
        self.driver.implicitly_wait(10)

    def shaping_base(self):
        # 競馬場情報
        self.keibajyou_dict = {
            "札幌":'01' ,"函館":'02' ,"福島":'03',
            "新潟":'04' ,"東京":'05' ,"中山":'06',
            "中京":'07' ,"京都":'08' ,"阪神":'09',
            "小倉":'10'
            }
        
        self.wether = {'晴':'sunny', '曇':'cloudy','雨': 'rain', '小雨':'light rain', '雪':'snowy', '小雪':'light snowy'}
        self.track_condition = {'良':'firm', '稍':'good', '重':'soft', '不良':'heavy'}
        self.racecourse_list = {
            '01':'Sapporo', '02':'Hakodate', '03':'Fukushima',
            '04':'Niigata', '05':'Tokyo', '06':'Nakayama',
            '07':'Chukyo', '08':'Kyoto', '09':'Hanshin',
            '10':'Kokura'}


class DayRaces(Base):

    # １日のレースデータ
    def date_races_list(self):
        print('start')
        self.scraping_base()

        date_now = str(datetime.date.today())
        date_now = date_now.split('-')

        year = date_now[0]
        # month = date_now[1]
        # day = date_now[2]
        month = '11'
        day = '27'
        url = "https://race.netkeiba.com/top/race_list.html?kaisai_date=" + year + month + day

        # urlから取得
        self.driver.get(url)
        # htlm変換
        html = self.driver.page_source.encode('utf-8')
        #　ドライバーを終了
        self.driver.quit()
        print(url)

        return year, html

    # １日のレースデータ整形
    def date_races_shaping(self):
        year, html = self.date_races_list()
        self.shaping_base()
        data_list = []

        # データがある時とない時の処理
        try:
            # textだけ取り出して配列に入れ不要な部分をsplitしている *lxmlでは動かない*
            soup = BeautifulSoup(html, 'html.parser')
            span =  soup.select_one('#RaceTopRace > div').get_text().strip()
            data = [i.strip() for i in span.split()]
            race_indexes = [i for i, x in enumerate(data) if x == "1R"]
            keibajyou_indexes = [i for i, x in enumerate(data) if x in self.keibajyou_dict.keys()]

            # raceidを求めて時間を分に統合
            for i in range(len(race_indexes)):
                for w in range(race_indexes[i], race_indexes[i] + 60, 5):
                    data_list.append([year
                                    + self.keibajyou_dict[data[keibajyou_indexes[i]]]
                                    + re.sub(r"\D", "", data[keibajyou_indexes[i] - 1]).zfill(2)
                                    + re.sub(r"\D", "", data[keibajyou_indexes[i] + 1]).zfill(2)
                                    + re.sub(r"\D", "", data[w]).zfill(2),
                                    int(data[w + 2][:2]) * 60 + (int(data[w + 2][3:]) - 10)])

            # 合計した時間は-10分されている
            # [['RaceID', 分], ・・・・]
            #分でソート
            return sorted(data_list, key = lambda x: x[1])
        except:
            return False


# レース単位
class OneRace(Base):

    def __init__(self, id=None):
        # 設定
        self.id = str(id)

        self.year = self.id[:4]
        self.keibajyou = self.id[4:6]
        self.kai = self.id[6:8]
        self.nichime = self.id[8:10]
        self.race = self.id[10:]

    # スクレイピング
    def race_data_scraping(self):
        print('start')  # 動作確認用

        self.scraping_base()

        url = 'https://race.netkeiba.com/race/shutuba.html?race_id=' +  self.id
        print(url)
        soup = BeautifulSoup(requests.get(url).content, 'lxml')
        span =  soup.select_one('#page > div.RaceColumn01 > div > div.RaceMainColumn > div.RaceList_NameBox > div.RaceList_Item02 > div.RaceData01').get_text().strip()
        self.race_data = [[j.strip() for j in i.split(':', 1)] for i in span.split('/')]
        self.driver.get(url)
        html = self.driver.page_source.encode('utf-8')

        #　ドライバーを終了
        self.driver.quit()

        return html

    # レース単位データ整形
    def data_shaping(self):
        html = self.race_data_scraping()
        self.shaping_base()

        def change_en(value_data):
            return  translator.translate(value_data).text

        def age(value_data):
            return int(value_data[1:])

        def gender(value_data):
            if value_data[:1] == '牡':
                return 'male'
            if value_data[:1] == '牝':
                return 'female'
            return 'gelding'

        def horse_weight(value_data):
            return int(value_data[:value_data.find('(')])
            
        def weight_cycling(value_data):
            return int(str(value_data[value_data.find('('):]).replace("(","").replace(")",""))

        def trainer(value_data):
            if value_data[:2] == '栗東':
                return str(value_data.replace('栗東', '[東]'))
            if value_data[:2] == '美浦':
                return str(value_data.replace('美浦', '[西]'))
            return str('none')

        translator = Translator()
        data_list = pd.DataFrame()
        
        data_new = pd.read_html(html, encoding='utf-8')[0]

        data_new.columns = [''.join(col) for col in data_new.columns.values]
        data_new = data_new.drop(columns= ['印印', 'お気に入り馬登録', 'お気に入り馬メモ'])
        data_new = data_new.set_axis(['枠番', '馬番', '馬名', '性齢', '斤量', '騎手', '調教師', '馬体重', '単勝', '人気'], axis=1)
        data_new = data_new.reindex(['枠番', '馬番', '馬名', '性齢', '斤量', '騎手', '単勝', '人気', '馬体重', '調教師'], axis=1)

        data_new = data_new.drop(data_new.index[(data_new['馬体重']=='--')])

        data_new['horse_name'] = data_new['馬名'].apply(change_en)
        data_new['jockey'] = data_new['騎手'].apply(change_en)
        data_new['調教師'] = data_new['調教師'].apply(trainer)
        data_new['trainer'] = data_new['調教師'].apply(change_en)
        data_new['age'] = data_new['性齢'].apply(age)
        data_new['gender'] = data_new['性齢'].apply(gender)
        data_new['horse_weight'] = data_new['馬体重'].apply(horse_weight)
        data_new['weight_cycling'] = data_new['馬体重'].apply(weight_cycling)
        data_new['racecourse'] = self.racecourse_list[self.keibajyou]
        data_new['turn'] = 'clockwise' if re.findall('(?<=\().+?(?=\))', str(self.race_data[1]))[0]  == '右' else 'anticlockwise'
        data_new['circumference'] = int(re.sub(r"\D", "", self.race_data[1][0]))
        data_new['wether'] = self.wether[self.race_data[2][1]]
        data_new['track_surface'] = 'grass' if self.race_data[1][0][:1]  == '芝' else 'dirt'
        data_new['track_condition'] = self.track_condition[self.race_data[3][1]]
        data_new['race_id'] = self.id
        data_new = data_new.rename(columns={'枠番':'bracket_number', '馬番':'horse_number', '斤量':'penalty', '単勝':'odds', '人気':'favorite'})
        data_new[['penalty', 'favorite']] = data_new[['penalty', 'favorite']].astype('int')
        data_new[['odds']] = data_new[['odds']].astype('float')
        data_new = data_new.drop(columns= ['馬名', '騎手', '調教師', '性齢', '馬体重'])

        data_list = pd.concat([data_list, data_new],ignore_index=True)

        data_list = data_list.reindex(columns=[
            'race_id','bracket_number',
            'horse_number','horse_name',
            'gender','age',
            'penalty','jockey',
            'trainer','horse_weight',
            'weight_cycling','odds',
            'favorite','racecourse',
            'track_surface','circumference',
            'turn','wether',
            'track_condition'])

        return data_list




