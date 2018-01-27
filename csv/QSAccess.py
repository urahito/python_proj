import os, sys
import pandas as pd

def main():
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

    df = pd.read_csv(file_path, encoding='Shift_JIS', index_col='Start', engine='python')

    df = df.rename(columns={'Start':'日付', \
            'Body Fat Percentage (%)': '体脂肪率', 'Weight (kg)': '体重'})  

    data = df[['体脂肪率', '体重']]
    data = data[data > 0]
    data = data.dropna()
    data['BMI'] = data['体重'] / (height ** 2)
    data['除脂肪体重'] = data['体重'] * (1 - data['体脂肪率'])
    data['基礎代謝'] = 370 + (21.6 * data['除脂肪体重'])
    print(data)
        
    data.to_csv(os.path.join(file_dir, 'HealthData_stat.csv'))
    
if __name__ == '__main__':
    main()