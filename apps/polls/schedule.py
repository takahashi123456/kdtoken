from .models import HorseModel, RacesTimeModel      # モデル呼出
from .scraping import *

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import AndTrigger, OrTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from googletrans import Translator
from pycaret.classification import *

import datetime
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
    merge.to_csv('/Users/nagatadaiki/Dropbox/My Mac (永田のMacBook Air)/Desktop/data_predict_' + 'sample' + '.csv')
    # merge.to_csv()
    # merge.to_json()

    print(merge)
    # predict_data = merge.to_json()
    return merge.to_json()

# データベースに予測結果を追加
def model_add(predict, race_data):
    sample = HorseModel(race_id = 6, score = predict(race_data))
    sample.save()
    print('OK')

# 関数をまとめる
def score_schedule_execute():
    start = time.time()
    shaping = ShapingRaceData()
    # model_add(predict_score, race_data_scraping)
    model_add(predict_score, shaping.data_shaping())
    end = time.time()
    print(end - start)

# １日の最初に実行 １日のレースを取ってくる
def date_farst_execute():
    start = time.time()
    shaping = ShapingRaceData()
    data_id_minute = shaping.date_races_shaping()

    # RaceTimeClassにデータ追加
    if data_id_minute:
        RacesTimeModel.objects.all().delete()

        for i in range(len(data_id_minute)):
            add_id_time = RacesTimeModel(race_id = data_id_minute[i][0],
                                         time_minute = data_id_minute[i][1])
            add_id_time.save()

    end = time.time()
    print(end - start)
    print(data_id_minute)


# 定期実行処理
def start():
    scheduler = BackgroundScheduler()

    def test():
        print(datetime.datetime.now())
        time_model = RacesTimeModel.objects.all()[0]
        print(time_model.race_id, time_model.time_minute)
        # print(len(time_model))
        # global cnt
        # cnt += 5
        # trigger = AndTrigger([IntervalTrigger(seconds=cnt)])
        # scheduler.reschedule_job('test01' , trigger=trigger, args=[], max_instances=1)

    def day_schedule_time_put():
        print('レース時間の指定完了')
        
        time_hour = [30, 31, 32, 33, 34]
        time_minute = [10, 20, 30, 40, 50]
        trigger_list = [CronTrigger(hour=time_hour[i], second=time_minute[i], jitter=5) for i in range(len(time_hour))]
        trigger = OrTrigger(trigger_list)
        scheduler.reschedule_job('test01' , trigger=trigger)
    
    # scheduler.add_job(predict, 'interval', seconds=10) # 処理時間の指定
    # scheduler.add_job(race_data_scraping, 'cron', hour=22, day_of_week='sat,sun') # 土曜と日曜の22時になると実行
    scheduler.add_job(date_farst_execute, 'cron', minute=58, max_instances=1)
    scheduler.add_job(score_schedule_execute, 'cron', minute = 55, id='', max_instances=1)
    scheduler.add_job(day_schedule_time_put,'cron', minute=43, max_instances=1)
    scheduler.add_job(test,'cron', minute=52, id='test01', max_instances=1)
    
    scheduler.start()
