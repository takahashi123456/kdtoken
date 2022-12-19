from bs4 import BeautifulSoup
import pandas as pd
import itertools
import datetime
import os
import time

from .models import *

#単勝
def tansyou(predict_data, odds_list1):
    list1_index = odds_list1[odds_list1[0].str.contains("単勝")].reset_index(drop=True)
    horse = int(list1_index[1][0])
    horse_odd = int(list1_index[2][0].replace("円", '').replace(",", ''))

    #予想
    predict = predict_data['horse_number'][predict_data['DeviationValue'].idxmax()]

    #掛け金と勝ち判定変数
    payout = -100
    win = 0

    #判定
    if horse == predict:
        payout += horse_odd
        win = 1
    else:
        pass
    
    #常に実行
    if True == True:
        tansyou_payout = payout
        tansyou_win = win
    
    return tansyou_payout, tansyou_win

#複勝
def hukusyou(predict_data, odds_list1):
    list1_index = odds_list1[odds_list1[0].str.contains("複勝")].reset_index(drop=True)
    horse_list = list(map(int, list1_index[1][0].split()))
    horse_odd_list = list(map(int, list(filter(None, list1_index[2][0].replace(",", '').split('円')))))

    #予想(リスト)
    predict_list = predict_data.nlargest(3, "DeviationValue", keep='all')["horse_number"].values.tolist()

    #掛け金と勝ち判定変数（複数掛け）
    payout = -100 * len(predict_list)
    win = 0

    #判定
    for i in range(len(horse_list)):
        if horse_list[i] in predict_list:
            payout += horse_odd_list[i]
            win += 1
        else:
            pass
    
    return payout, win

#馬連
def umaren(predict_data, odds_list1):
    list1_index = odds_list1[odds_list1[0].str.contains("馬連")].reset_index(drop=True)
    horse_list = list(map(int, list1_index[1][0].split()))
    horse_odd = int(list1_index[2][0].replace("円", '').replace(",", ''))

    #予想(リスト)
    predict_list = [list(v) for v in itertools.combinations(predict_data.nlargest(4, "DeviationValue", keep='all')["horse_number"].values.tolist(), 2)]

    #掛け金と勝ち判定変数（複数掛け）
    payout = -100 * len(predict_list)
    win = 0

    #判定
    if horse_list in predict_list:
        payout += horse_odd
        win += 1
    elif horse_list[::-1] in predict_list:
        payout += horse_odd
        win += 1
    else:
        pass

    return payout, win

















#フォルダ内のファイル名をリストに入れている
csv_path = os.path.dirname(os.path.abspath(__file__)) + '/predict_csv/'
# path = "/content/drive/Shareddrives/keiba_lab/Team4/horse_racing/racing_data/payout_test/20221126"
files = os.listdir(csv_path)

#初期値
tansyou_sum = 0
tansyou_win = 0

hukusyou_sum = 0
hukusyou_win = 0

umaren_sum = 0
umaren_win = 0

date_now = str(datetime.date.today())
date_now = date_now.split('-')

year = date_now[0]
month = date_now[1]

bets = [tansyou, hukusyou, umaren]
models_name = ['lr']

# データベースに追加
def total_money_add():

    for bet in bets:
        total_money, win = bet(predict_data, odds_list1)

        for model_name in models_name:
            
            try:
                score = score = ModelScore.objects.get(
                    model_name=model_name, year=int(year),
                    month=int(month), bazyou='',
                    how_to_bet=str(bet))
                
                win = score.win + win
                race = score.race + 1
                total_money = score.total_money + total_money

            except User.DoesNotExist: # 存在しない場合
                ModelScore.objects.create(
                    model_name=model_name, year=int(year), month=int(month),
                    bazyou='', how_to_bet=str(bet), total_money='',
                    win='', race='', accuracy='',
                    recovery='')

    # model_name = models.CharField(max_length = 100, blank = True, null = True)
    # year = models.IntegerField()
    # month = models.IntegerField()
    # bazyou = models.CharField(max_length = 100, blank = True, null = True)
    # how_to_bet = models.CharField(max_length = 100, blank = True, null = True) # 賭け方
    # total_money = models.BigIntegerField(default=0)
    # win = models.IntegerField(default=0)
    # race = models.IntegerField(default=0)
    # accuracy = models.FloatField(default=0) # 的中率
    # recovery = models.FloatField(default=0) # 回収率

for i in range(len(files)):
    #スクレイピング
    predict_data = pd.read_csv(csv_path + "/"+ files[i], index_col=0)
    url = 'https://race.netkeiba.com/race/result.html?race_id=' + str(predict_data["race_id"][0])
    data = pd.read_html(url)[0]
    odds_list1 = pd.read_html(url)[1]

    tansyou_sum += tansyou(predict_data, odds_list1)[0]
    tansyou_win += tansyou(predict_data, odds_list1)[1]

    hukusyou_sum += hukusyou(predict_data, odds_list1)[0]
    hukusyou_win += hukusyou(predict_data, odds_list1)[1]

    umaren_sum += umaren(predict_data, odds_list1)[0]
    umaren_win += umaren(predict_data, odds_list1)[1]
    
    time.sleep(1)

#以下結果
# print("ファイル数：" + str(len(files)))
# print("--単勝--")
# print("投資金額：" + str(100 * len(files)) + "円")
# print("払い戻し：" + str((100 * len(files)) + tansyou_sum) + "円")
# print("結果：" + str(tansyou_sum) + "円")
# print("回収率：" + str(round(((100 * len(files) + tansyou_sum) / (100 * len(files)) * 100), 2)) + "％")
# print("的中率：" + str(round((tansyou_win / len(files) * 100), 2)) + "％")
# print("--複勝--")
# print("投資金額：" + str(300 * len(files)) + "円")
# print("払い戻し：" + str((300 * len(files)) + hukusyou_sum) + "円")
# print("結果：" + str(hukusyou_sum) + "円")
# print("回収率：" + str(round(((300 * len(files) + hukusyou_sum) / (300 * len(files)) * 100), 2)) + "％")
# print("的中率：" + str(round((hukusyou_win / len(files) / 3 * 100), 2)) + "％")
# print("--馬連--")
# print("投資金額：" + str(600 * len(files)) + "円")
# print("払い戻し：" + str((600 * len(files)) + umaren_sum) + "円")
# print("結果：" + str(umaren_sum) + "円")
# print("回収率：" + str(round(((600 * len(files) + umaren_sum) / (600 * len(files)) * 100), 2)) + "％")
# print("的中率：" + str(round((umaren_win / len(files) / 6 * 100), 2)) + "％")