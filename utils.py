import pandas as pd


def load_data(file_path):
    """加载数据"""
    try:
        data = pd.read_excel(file_path)
        data["日期"] = pd.to_datetime("1899-12-30") + pd.to_timedelta(data["日期"], "D")
        data.set_index("日期", inplace=True)
        return data
    except Exception as e:
        print(f"加载数据时发生错误: {e}")
        return None


def save_results(data, output_path):
    """保存预测结果到 Excel 文件"""
    try:
        data.to_excel(output_path, index=False)
        print(f"预测结果已保存到: {output_path}")
    except Exception as e:
        print(f"保存结果时发生错误: {e}")
