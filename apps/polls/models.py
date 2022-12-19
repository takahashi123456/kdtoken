from django.db import models

class SampleModel(models.Model):
    # APIが提供するデータ項目
    title = models.CharField(max_length = 100, blank = True, null = True)
    description = models.CharField(max_length = 300, blank = True, null = True)

    def __str__(self):
        return self.title

# レースidと予測結果
class HorseModel(models.Model):

    race_id = models.IntegerField(primary_key=True)
    score = models.TextField()

    def __int__(self):
        return self.race_id

# レースidと時間
class RacesTimeModel(models.Model):
    race_id = models.IntegerField()
    time_minute = models.IntegerField()

    def __str__(self):
        return f'id:{self.race_id}, minute:{self.time_minute}'

# 的中率、回収率
# class RaceModelScore(models.model):
#     model_name = 


# 的中率、回収率
# 旧データベースのため以下不使用
class ModelScore(models.Model):
    model_name = models.CharField(max_length = 100, blank = True, null = True)
    year = models.IntegerField()
    month = models.IntegerField()
    bazyou = models.CharField(max_length = 100, blank = True, null = True)
    how_to_bet = models.CharField(max_length = 100, blank = True, null = True) # 賭け方
    total_money = models.BigIntegerField(default=0)
    win = models.IntegerField(default=0)
    race = models.IntegerField(default=0)
    accuracy = models.FloatField(default=0) # 的中率
    recovery = models.FloatField(default=0) # 回収率

    def __str__(self):
        return f'モデル名：{self.model_name}, {self.year}年{self.month}月, 馬場：{self.bazyou}'

