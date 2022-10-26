from .models import HorseModel                         # モデル呼出
from rest_framework import generics   # API
from rest_framework import viewsets
# from django_filters.rest_framework import DjangoFilterBackend
from .serializers import SampleSerializer                # APIで渡すデータをJSON,XML変換

class api(generics.ListAPIView):
# class api(generics.ListCreateAPIView):
    # 対象とするモデルのオブジェクトを定義
    queryset = HorseModel.objects.all()

    # APIがデータを返すためのデータ変換ロジックを定義
    serializer_class = SampleSerializer

    # 認証
    permission_classes = []
    

class DetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HorseModel.objects.all()
    serializer_class = SampleSerializer