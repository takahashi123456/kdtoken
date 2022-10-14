from .models import SampleModel                         # モデル呼出
from rest_framework import generics   # API
from rest_framework import viewsets
# from django_filters.rest_framework import DjangoFilterBackend
from .serializers import SampleSerializer                # APIで渡すデータをJSON,XML変換

class api(generics.ListAPIView):
    # 対象とするモデルのオブジェクトを定義
    queryset = SampleModel.objects.all()

    # APIがデータを返すためのデータ変換ロジックを定義
    serializer_class = SampleSerializer

    # 認証
    permission_classes = []

    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['id','title']   # フィルターで特定の情報のみ取得可能


# class test(viewsets.ReadOnlyModelViewSet):
#     # 対象とするモデルのオブジェクトを定義
#     queryset = SampleModel.objects.all()
#     # APIがデータを返すためのデータ変換ロジックを定義
#     serializer_class = SampleSerializer

#     # filter_fields = ('id','title')   # フィルターで特定の情報のみ取得可能
    

class DetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SampleModel.objects.all()
    serializer_class = SampleSerializer