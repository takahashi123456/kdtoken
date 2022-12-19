from .models import HorseModel, RacesTimeModel      # モデル呼出
from .scraping import ScrapingData
from .predict import *

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import AndTrigger, OrTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

import datetime
import time

scraping_data = ScrapingData()

# １日の最初に実行 １日のレースを取ってくる
def date_farst_execute():
    start = time.time()
    data_id_minute = scraping_data.day_races_get()
    RacesTimeModel.objects.all().delete()

    # RaceTimeClassにデータ追加
    if data_id_minute:
        print('OK')

        for i in range(len(data_id_minute)):
            add_id_time = RacesTimeModel(race_id = data_id_minute[i][0],
                                         time_minute = data_id_minute[i][1])
            add_id_time.save()

    end = time.time()
    print(end - start)

# レースの予測
def score_schedule_execute(id):
    start = time.time()
    scraping_get = scraping_data.one_race_get(id)
    predict_get = PredictRace()
    
    predict_get.model_add(scraping_get, id)
    end = time.time()
    print(end - start)

# 定期実行処理
def start():
    scheduler = BackgroundScheduler()
    id_time_model = RacesTimeModel.objects.all()

    def id_update(cnt):
        print('update')
        try:
            print(cnt)
            print(type(cnt))
            race_id = id_time_model[cnt].race_id
            score_schedule_execute(race_id)
            scheduler.modify_job('schedule_predict', args=[cnt+1])
            print('count')
        except:
            scheduler.modify_job('schedule_predict', args=[cnt+1])
            print('skipp')
    
    # 定期実行時間の更新
    def day_schedule_time_apdate():
        for time_model in id_time_model:
            print(time_model.time_minute // 60, time_model.time_minute % 60)

        trigger_list = [CronTrigger(hour=time_model.time_minute // 60,
                                    minute=time_model.time_minute % 60, 
                                    jitter=60)
                                    for time_model in id_time_model]
        trigger = OrTrigger(trigger_list)

        scheduler.reschedule_job('schedule_predict' , trigger=trigger)
        scheduler.modify_job('schedule_predict', args=[0])
        print(datetime.datetime.now(), ':OK')

    def test(cnt):
        print('update')
        try:
            print(cnt)
            race_id = id_time_model[cnt].race_id
            score_schedule_execute(race_id)
            scheduler.modify_job('test', args=[cnt+1])
            print('count')
            print('---------')
        except:
            scheduler.modify_job('test', args=[cnt+1])
            print('next')
            print('---------')

    # 本番↓
    scheduler.add_job(date_farst_execute, 'cron', hour=8, minute=0, max_instances=1)
    scheduler.add_job(id_update, 'cron', year=2022, month=12, day=19, args=[0], id='schedule_predict', max_instances=5) # 変更前提 基本実行されない
    scheduler.add_job(day_schedule_time_apdate, 'cron', hour=8, minute=30, max_instances=1)

    # テスト↓
    # scheduler.add_job(date_farst_execute, 'cron', minute=31, max_instances=1)
    # scheduler.add_job(test, 'interval', minutes=1, args=[0], jitter=60, id='test', max_instances=5)
    # scheduler.add_job(test, 'cron', minute=1, args=[22], jitter=60, id='test', max_instances=5)
    # scheduler.add_job(score_schedule_execute, 'cron', minute=57, args=[202209050102], max_instances=1)
    
    scheduler.start()
