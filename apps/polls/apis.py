from .models import SampleModel                         # モデル呼出
from rest_framework import generics   # API
from .serializers import SampleSerializer                # APIで渡すデータをJSON,XML変換

class api(generics.ListCreateAPIView):
    # 対象とするモデルのオブジェクトを定義
    queryset = SampleModel.objects.all()

    # APIがデータを返すためのデータ変換ロジックを定義
    serializer_class = SampleSerializer

    # 認証
    permission_classes = []
    

class DetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SampleModel.objects.all()
    serializer_class = SampleSerializer