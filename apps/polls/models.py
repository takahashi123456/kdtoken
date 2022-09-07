from django.db import models

class SampleModel(models.Model):
    # APIが提供するデータ項目
    title = models.CharField(max_length = 100)
    description = models.CharField(max_length = 300)

    def __str__(self):
        return self.title

