from .models import SampleModel                         # モデル呼出
from datetime import datetime, date
from apscheduler.schedulers.background import BackgroundScheduler

from bs4 import BeautifulSoup
from googletrans import Translator
from pycaret.classification import *
from selenium import webdriver
import chromedriver_binary
import requests
import pandas as pd
import numpy as np
import os
import glob
import re
import time


def scraping(): # スクレイピング処理
  # print('start')  # 動作確認用
    # 設定 #

  year =2022
  keibajyou = 6
  kai = 4
  nichime = 1
  race = 10

  #

  def change_en(original):
      return  translator.translate(original).text

  def age(original):
      return int(original[1:])

  def gender(original):
      if original[:1] == '牡':
          return 'male'
      elif original[:1] == '牝':
          return 'female'
      else :
          return 'gelding'

  def horse_weight(original):
      return int(original[:original.find('(')])
      
  def weight_cycling(original):
      return int(str(original[original.find('('):]).replace("(","").replace(")",""))

  def trainer(original):
      if original[:2] == '栗東':
          return str(original.replace('栗東', '[東]'))
      elif original[:2] == '美浦':
          return str(original.replace('美浦', '[西]'))
      else :
          return str('none')

  translator = Translator()
  data_list = pd.DataFrame()

  wether = {'晴':'sunny', '曇':'cloudy','雨': 'rain', '小雨':'light rain', '雪':'snowy', '小雪':'light snowy'}
  track_condition = {'良':'firm', '稍重':'good', '重':'soft', '不良':'heavy'}
  racecourse_list = {'01':'Sapporo', '02':'Hakodate', '03':'Fukushima', '04':'Niigata', '05':'Tokyo', '06':'Nakayama', '07':'Chukyo', '08':'Kyoto', '09':'Hanshin', '10':'Kokura'}

  keibajyou_list = ['01','02','03','04','05','06','07','08','09','10']
  kai_list = ['01','02','03','04','05','06']
  nichime_list = ['01','02','03','04','05','06','07','08','09','10','11','12']
  race_list = ['01','02','03','04','05','06','07','08','09','10','11','12']

  url = 'https://race.netkeiba.com/race/shutuba.html?race_id=' +  str(year) + str(keibajyou_list[keibajyou]) + str(kai_list[kai]) + str(nichime_list[nichime]) + str(race_list[race])

  soup = BeautifulSoup(requests.get(url).content, 'lxml')
  span =  soup.select_one('#page > div.RaceColumn01 > div > div.RaceMainColumn > div.RaceList_NameBox > div.RaceList_Item02 > div.RaceData01').get_text().strip()
  race_data = [[j.strip() for j in i.split(':', 1)] for i in span.split('/')]

  options = webdriver.ChromeOptions()
  options.add_argument('--headless')
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome('chromedriver',options=options)
  driver.implicitly_wait(10)

  driver.get(url)

  html = driver.page_source.encode('utf-8')
  data_new = pd.read_html(html, encoding='utf-8')[0]

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
  data_new['racecourse'] = str(racecourse_list[str(keibajyou_list[keibajyou])])
  data_new['turn'] = 'clockwise' if re.findall('(?<=\().+?(?=\))', str(race_data[1]))[0]  == '右' else 'anticlockwise'
  data_new['circumference'] = int(re.sub(r"\D", "", race_data[1][0]))
  data_new['wether'] = wether[race_data[2][1]]
  data_new['track_surface'] = 'grass' if race_data[1][0][:1]  == '芝' else 'dirt'
  data_new['track_condition'] = track_condition[race_data[3][1]]
  data_new['race_id'] = str(year) + str(keibajyou_list[keibajyou]) + str(kai_list[kai]) + str(nichime_list[nichime]) + str(race_list[race])
  data_new = data_new.rename(columns={'枠番':'bracket_number', '馬番':'horse_number', '斤量':'penalty', '単勝':'odds', '人気':'favorite'})
  data_new[['penalty', 'favorite']] = data_new[['penalty', 'favorite']].astype('int')
  data_new[['odds']] = data_new[['odds']].astype('float')
  data_new = data_new.drop(columns= ['馬名', '騎手', '調教師', '性齢', '馬体重'])

  data_list = pd.concat([data_list, data_new],ignore_index=True)

  data_list = data_list.reindex(columns=['race_id', 'bracket_number', 'horse_number', 'horse_name', 'gender', 'age', 'penalty', 'jockey', 'trainer', 'horse_weight', 'weight_cycling', 'odds', 'favorite', 'racecourse', 'track_surface', 'circumference', 'turn', 'wether', 'track_condition'])

  # data_list.to_csv('[PATHを指定]' + str(year) + str(keibajyou_list[keibajyou]) + str(kai_list[kai]) + str(nichime_list[nichime]) + str(race_list[race]) + '.csv')
  # /Users/nagatadaiki/Dropbox/My Mac (永田のMacBook Air)/Desktop/アプリ開発
  # print(data_list)
  return data_list

# 予測
def predict():
  path = os.path.dirname(__file__) + '/predict_models/2021_lr'
  model = load_model(path)
  data_predict = scraping()

  result = predict_model(model, data = data_predict)

  result_d = result.loc[:, ['horse_number', 'prediction_label', 'prediction_score']].sort_values('horse_number').reset_index(drop=True)

  print(result_d)

# 定期実行処理
def start():
  scheduler = BackgroundScheduler()
  # scheduler.add_job(predict, 'interval', seconds=10) # 処理時間の指定
  # scheduler.add_job(scraping, 'cron', hour=22, day_of_week='sat,sun') # 土曜と日曜の22時になると実行
  scheduler.add_job(predict, 'cron', minute = 46)
  scheduler.start()