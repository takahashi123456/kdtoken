from .models import HorseModel      # モデル呼出

from pycaret.classification import *

import pandas as pd
import numpy as np
import os

class PredictRace:
    # 予測
    def predict_score(self, race_data, id):   #　引数にスクレイピングしたレース情報
        # スコアの表示を整える
        def score_shaping(oneline_data):
            if oneline_data['prediction_label'] == 0:
                return 1 - oneline_data['prediction_score']
            if oneline_data['prediction_label'] == 1:
                return oneline_data['prediction_score']
            return str("None")
        
        path = os.path.dirname(__file__) + '/predict_models/2021_lr'
        model = load_model(path)

        result = predict_model(model, data=race_data)

        result['score'] = result.apply(score_shaping,axis=1)
        score_std = result['score'].std(ddof=0)
        score_mean = result['score'].mean()
        result['DeviationValue'] = result['score'].map(lambda x: round((x - score_mean) / score_std * 10 + 50, 2))

        merge = pd.merge(race_data, result['DeviationValue'], right_index=True, left_index=True)
        merge.to_csv('/Users/nagatadaiki/Dropbox/My Mac (永田のMacBook Air)/Desktop/csv_data/' + str(id) + '.csv')
        # merge.to_csv()
        # merge.to_json()

        print(merge)
        # predict_data = merge.to_json()
        return merge.to_json()

    # データベースに予測結果を追加
    def model_add(self, race_data, id):
        sample = HorseModel(race_id=id, score=self.predict_score(race_data, id))
        sample.save()
        print('OK')