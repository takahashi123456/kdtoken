from datetime import datetime, date
from apscheduler.schedulers.background import BackgroundScheduler


def update():# 任意の関数名
    print('update')

def start():
  scheduler = BackgroundScheduler()
  scheduler.add_job(update, 'interval', seconds=10) # 処理時間の指定
  scheduler.start()