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
    score = models.FloatField(blank = True, null = True)

    def __str__(self):
        return self.race_id

