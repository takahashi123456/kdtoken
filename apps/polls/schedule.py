from .models import HorseModel, RacesTimeModel      # モデル呼出
from .scraping import *
from .predict import *

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import AndTrigger, OrTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

import datetime
import time

# 関数をまとめる
def score_schedule_execute(id):
    start = time.time()
    scraping_get = ShapingRaceData(id)
    predict_get = PredictRace()
    # race_id = 202209050102
    
    predict_get.model_add(scraping_get.data_shaping(), id)
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
    # print(data_id_minute)

# 定期実行処理
def start():
    scheduler = BackgroundScheduler()
    id_time_model = RacesTimeModel.objects.all()

    def sample(cnt):
        print(cnt)
        race_id = id_time_model[cnt].race_id
        print(type(race_id))
        print(race_id)
        scheduler.modify_job('test01', args=[cnt+1])

    def id_update(cnt):
        print('update')
        # try:
        print(cnt)
        print(type(cnt))
        race_id = id_time_model[cnt].race_id
        score_schedule_execute(race_id)
        scheduler.modify_job('schedule_predict', args=[cnt+1])
        print('count')
        # except:
        #     scheduler.modify_job('schedule_predict', args=[0])
        #     print('riset')
    
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
        print(datetime.datetime.now(), ':OK')

    # 定期実行時間の更新
    def test():
        for time_model in id_time_model:
            print(time_model.time_minute // 60, time_model.time_minute % 60)

        trigger_list = [CronTrigger(minute=time_model.time_minute // 60,
                                    second=time_model.time_minute % 60, 
                                    jitter=60)
                                    for time_model in id_time_model]
        trigger = OrTrigger(trigger_list)

        scheduler.reschedule_job('test01' , trigger=trigger)
        print(datetime.datetime.now(), ':OK')
    
    # scheduler.add_job(date_farst_execute, 'cron', minute=58, max_instances=1)
    # scheduler.add_job(score_schedule_execute, 'cron', minute=32, id='schedule_predict', max_instances=5)
    scheduler.add_job(id_update, 'cron', day=30, args=[0], id='schedule_predict', max_instances=5)
    # scheduler.add_job(test, 'cron', minute=29, max_instances=1)
    scheduler.add_job(day_schedule_time_apdate, 'cron', minute=43, max_instances=1)
    # scheduler.add_job(sample,'cron', day=28, args=[0], id='test01', max_instances=10)
    # scheduler.add_job(sample,'interval', seconds=10, args=[0], id='test01', max_instances=1)
    # scheduler.add_job(test,'cron', minute=15, max_instances=1)
    # scheduler.add_job(sample, 'interval', seconds=10, args=[1], id='test02', max_instances=1)
    
    scheduler.start()
