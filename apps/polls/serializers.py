#  APIの出力をJSON,XMLデータに変換
from rest_framework import serializers
from .models import SampleModel

class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleModel                    # 呼び出すモデル
        # fields = ["id", "label","score", "horse_number", "favorite", "horse_name", "jockey"]  # API上に表示するモデルのデータ項目
        fields = ["id", "title", "description"]
        # fields = '__all__'
