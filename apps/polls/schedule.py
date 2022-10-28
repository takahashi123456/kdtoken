from .models import SampleModel, HorseModel                       # モデル呼出
from datetime import datetime, date
from apscheduler.schedulers.background import BackgroundScheduler
from .scraping import RaceScraping

from bs4 import BeautifulSoup
from googletrans import Translator
from pycaret.classification import *
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

# 予測
def predict_score(race_data):   #　引数にスクレイピングしたレース情報
    # スコアの表示を整える
    def score(self):
        if self['prediction_label'] == 0:
            return 1 - self['prediction_score']
        elif self['prediction_label'] == 1:
            return self['prediction_score']
        else :
            return str("none")
    
    path = os.path.dirname(__file__) + '/predict_models/2021_lr'
    model = load_model(path)    # 予測モデルのパス

    result = predict_model(model, data = race_data)

    result['score'] = result.apply(score,axis=1)
    score_std = result['score'].std(ddof=0)
    score_mean = result['score'].mean()
    result['DeviationValue'] = result['score'].map(lambda x: round((x - score_mean) / score_std * 10 + 50, 2))

    merge = pd.merge(race_data, result['DeviationValue'], right_index=True, left_index=True)

    # merge.to_csv()
    # merge.to_json()

    # print(merge.to_json())
    predict_data = merge.to_json()
    return predict_data

# データベースに予測結果を追加
def model_add(predict, race_data):
    sample = HorseModel(race_id = 4, score = predict(race_data))
    sample.save()
    print('OK')

# 関数をまとめる
def score_schedule_execute():
    # model_add(predict_score, race_data_scraping)
    model_add(predict_score, RaceScraping().data_shape())

# 定期実行処理
def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(predict, 'interval', seconds=10) # 処理時間の指定
    # scheduler.add_job(race_data_scraping, 'cron', hour=22, day_of_week='sat,sun') # 土曜と日曜の22時になると実行
    scheduler.add_job(score_schedule_execute, 'cron', hour=9, minute = 40)
    scheduler.start()