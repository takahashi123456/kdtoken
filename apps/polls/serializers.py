#  APIの出力をJSON,XMLデータに変換
from rest_framework import serializers
from .models import SampleModel

class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleModel                    # 呼び出すモデル
        fields = '__all__' # API上に表示するモデルのデータ項目
        # fields = ('id', 'title')
        # read_only_fields = ('id', 'title', 'description')  # 読み取り専用
