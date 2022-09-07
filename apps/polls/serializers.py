#  APIの出力をJSON,XMLデータに変換
from rest_framework import serializers
from .models import SampleModel

class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleModel                     # 呼び出すモデル
        fields = ["id","title", "description"]  # API上に表示するモデルのデータ項目