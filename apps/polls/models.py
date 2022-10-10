from django.db import models

class SampleModel(models.Model):
    # APIが提供するデータ項目
    title = models.CharField(max_length = 100, blank = True, null = True)
    description = models.CharField(max_length = 300, blank = True, null = True)

    def __str__(self):
        return self.title

class HorseModel(models.Model):
    # APIが提供するデータ項目
    label = models.IntegerField(blank = True, null = True)
    score = models.FloatField(blank = True, null = True)
    horse_number = models.IntegerField(blank = True, null = True)
    favorite = models.IntegerField(blank = True, null = True)
    horse_name = models.CharField(max_length = 100, blank = True, null = True)
    jockey = models.CharField(max_length = 100, blank = True, null = True)

    def __str__(self):
        return self.horse_name

