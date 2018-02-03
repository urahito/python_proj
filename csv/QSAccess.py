import os, sys
import pandas as pd

def main():
    '''
    処理内容: 体脂肪率, 体重から計算した値を新たなcsvファイルに追加する

    コマンドライン引数
    引数0: このスクリプトのパス
    引数1: 読み込むcsvファイル => 'Body Fat Percentage (%)', 'Weight (kg)'が含まれるもの
    引数2: 身長(cm)
    '''
    argv = sys.argv

    # 引数の条件設定
    # 引数が3つか
    if len(argv) != 3:
        return
    # 引数1がファイルか
    elif not os.path.isfile(argv[1]):
        return
    # 引数2が数値で100以上か
    elif not argv[2].isdigit() and not argv[2] >= 100:
        return

    # 引数からの値の設定
    file_path = argv[1]
    file_dir, file_name = os.path.split(file_path)
    height = int(argv[2]) / 100.0

    # csvをデータフレームに展開
    df = pd.read_csv(file_path, encoding='Shift_JIS', index_col='Start', engine='python')

    # データフレーム上の列名を変更
    df = df.rename(columns={'Start':'日付', \
            'Body Fat Percentage (%)': '体脂肪率', 'Weight (kg)': '体重'})  

    # データフレームの値列を体脂肪率と体重に絞る
    data = df[['体脂肪率', '体重']]

    # 0は欠損値として扱い、そのレコードを削除する
    data = data[data > 0]
    data = data.dropna()

    # BMI、除脂肪体重、基礎代謝(Katch-McArdle式:除脂肪体重から算出する式)を求める
    data['BMI'] = data['体重'] / pow(height, 2)
    data['除脂肪体重'] = data['体重'] * (1 - data['体脂肪率'])
    data['基礎代謝'] = 370 + (21.6 * data['除脂肪体重'])
        
    # 結果csvファイルに書き出す
    data.to_csv(os.path.join(file_dir, 'HealthData_stat.csv'))
    
if __name__ == '__main__':
    main()