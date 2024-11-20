import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import rcParams

# 设置全局字体，使用黑体，确保中文显示正常
rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
rcParams['axes.unicode_minus'] = False    # 解决负号显示为方块的问题

def plot_predictions(data, prediction_results, chart_output_path, append_output):
    """绘制预测图表并保存"""
    y_columns = data.columns  # 动态获取所有列名

    # 动态设置子图数量，根据列数确定
    fig, axes = plt.subplots(nrows=len(y_columns), ncols=1, figsize=(12, 6 * len(y_columns)))
    if len(y_columns) == 1:
        axes = [axes]

    for i, region in enumerate(y_columns):
        # 绘制实际值
        axes[i].plot(data.index, data[region], label=f'{region} 本月实际值', color='blue', linewidth=2)

        # 绘制预测值（从本月结束后开始）
        future_dates = pd.to_datetime(prediction_results['日期'])
        prediction_values = prediction_results[region].values

        axes[i].plot(future_dates, prediction_values, label=f'{region} 下月预测值', linestyle='--', color='orange', linewidth=2)

        # 设置图表标题和标签，指定支持中文的字体
        axes[i].set_title(f'{region} 燃气使用情况', fontsize=14, fontname='SimHei')
        axes[i].legend(fontsize=10, prop={'family': 'SimHei'})
        axes[i].set_xlabel('日期', fontsize=12, fontname='SimHei')
        axes[i].set_ylabel('使用量', fontsize=12, fontname='SimHei')

        # 调整X轴标签以避免重叠
        axes[i].tick_params(axis='x', rotation=45)

        # 根据数据适当调整y轴的范围
        y_min, y_max = data[region].min(), max(data[region].max(), prediction_values.max())
        axes[i].set_ylim([y_min * 0.9, y_max * 1.1])

    fig.tight_layout()
    fig.savefig(chart_output_path)
    append_output(f"预测图表已保存到 {chart_output_path}")