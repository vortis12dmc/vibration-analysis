import sys
import pandas as pd
import statistics

def analyze_frequency_ranges(df, axis):
    ranges = [(1250, 1350), (2500, 2600)]
    axis_data = df[df['Axis'] == axis]

    for r in ranges:
        range_data = axis_data[(axis_data['Frequency[Hz]'] >= r[0]) & (axis_data['Frequency[Hz]'] < r[1])]

        if not range_data.empty:
            # 周波数に対する解析
            # 平均値
            avg_freq = range_data['Frequency[Hz]'].mean()
            # 最頻値
            mode_freq = range_data['Frequency[Hz]'].value_counts().idxmax()
            # 分散値
            var_freq = statistics.variance(range_data['Frequency[Hz]'])
            # 標準偏差
            std_dev_freq = statistics.stdev(range_data['Frequency[Hz]'])

            # パワーに対する解析
            # 平均値
            avg_value = range_data['Power'].mean()
            # 最頻値
            mode_value = range_data['Power'].value_counts().idxmax()
            # 分散値
            var_value = statistics.variance(range_data['Power'])
            # 標準偏差
            std_dev_value = statistics.stdev(range_data['Power'])

            count = len(range_data)
            print(f"Axis {axis} - Range {r[0]}Hz to {r[1]}Hz: "
                  f"Avg Frequency: {avg_freq}, "
                  f"Mode Frequency: {mode_freq}, "
                  + "\n\t\t\t\t " + f"Var Frequency: {var_freq}, "
                  f"Std Dev Frequency: {std_dev_freq}, "
                  + "\n\t\t\t\t " + f"Avg Value: {avg_value}, "
                  f"Mode Value: {mode_value}, "
                  + "\n\t\t\t\t " + f"Var Value: {var_value}, "
                  f"Std Dev Value: {std_dev_value}, "
                  f"Count: {count}")
        else:
            print(f"Axis {axis} - Range {r[0]}Hz to {r[1]}Hz: No data available")

def analyze_csv(file_path):
    # CSVファイルを読み込む
    df = pd.read_csv(file_path)

    sprit_readFile = file_path.split('/')
    sensor_name = sprit_readFile[5].replace("_noiseidentify.csv", "")
    print("\t\t-- " + sensor_name + " --\n")
    
    # 各軸についての平均ピーク周波数と値を計算
    for axis in ['X', 'Y', 'Z']:
        axis_data = df[df['Axis'] == axis]
        if not axis_data.empty and 'Power' in axis_data.columns:
            avg_freq = axis_data['Frequency[Hz]'].mean()
            avg_value = axis_data['Power'].mean()
            print(f"Axis {axis} - Average Frequency: {avg_freq}, Average Value: {avg_value}")
        else:
            print(f"Axis {axis} - No data available or 'Value' column missing")

    # 特定の周波数範囲でのデータに焦点を当てる（例：1000Hz以上）
    filtered_data = df[df['Frequency[Hz]'] >= 1000]
    for axis in ['X', 'Y', 'Z']:
        axis_data = filtered_data[filtered_data['Axis'] == axis]
        if not axis_data.empty and 'Power' in axis_data.columns:
            avg_freq = axis_data['Frequency[Hz]'].mean()
            avg_value = axis_data['Power'].mean()
            print(f"Axis {axis} (1000Hz以上) - Average Frequency: {avg_freq}, Average Value: {avg_value}")
        else:
            print(f"Axis {axis} (1000Hz以上) - No data available or 'Value' column missing")

    # 各軸ごとに周波数範囲を分析
    for axis in ['X', 'Y', 'Z']:
        analyze_frequency_ranges(df, axis)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python <script_name>.py <csv_file_path>")
        sys.exit(1)

    csv_file_path = sys.argv[1]
    analyze_csv(csv_file_path)

