import sys
import pandas as pd

def analyze_frequency_ranges(df, axis):
    ranges = [(0, 500), (500, 1000), (1000, float('inf'))]
    axis_data = df[df['Axis'] == axis]

    for r in ranges:
        range_data = axis_data[(axis_data['Frequency'] >= r[0]) & (axis_data['Frequency'] < r[1])]
        avg_freq = range_data['Frequency'].mean()
        avg_value = range_data['Value '].mean()
        count = len(range_data)
        print(f"Axis {axis} - Range {r[0]}Hz to {r[1]}Hz: Average Frequency: {avg_freq}, Average Value: {avg_value}, Count: {count}")

def analyze_csv(file_path):
    # CSVファイルを読み込む
    df = pd.read_csv(file_path)

    # 各軸についての平均ピーク周波数と値を計算
    for axis in ['X', 'Y', 'Z']:
        axis_data = df[df['Axis'] == axis]
        if not axis_data.empty and 'Value ' in axis_data.columns:
            avg_freq = axis_data['Frequency'].mean()
            avg_value = axis_data['Value '].mean()
            print(f"Axis {axis} - Average Frequency: {avg_freq}, Average Value: {avg_value}")
        else:
            print(f"Axis {axis} - No data available or 'Value' column missing")

    # 特定の周波数範囲でのデータに焦点を当てる（例：1000Hz以上）
    filtered_data = df[df['Frequency'] >= 1000]
    for axis in ['X', 'Y', 'Z']:
        axis_data = filtered_data[filtered_data['Axis'] == axis]
        if not axis_data.empty and 'Value ' in axis_data.columns:
            avg_freq = axis_data['Frequency'].mean()
            avg_value = axis_data['Value '].mean()
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

