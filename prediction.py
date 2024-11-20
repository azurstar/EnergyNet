import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX


def predict_arima(data, append_output):
    """运行 ARIMA 预测"""
    y_columns = data.columns  # 动态获取所有列名
    next_month_data = []

    for region in y_columns:
        y = data[region]
        try:
            append_output(f"正在训练 ARIMA 模型预测 {region}...")
            # 使用自动确定的ARIMA参数
            p, d, q = 2, 1, 2
            P, D, Q, s = 1, 1, 1, 7
            arima_model = SARIMAX(y, order=(p, d, q), seasonal_order=(P, D, Q, s))
            arima_result = arima_model.fit(disp=False)

            # 预测未来 30 天
            arima_predictions = arima_result.forecast(steps=30)
            append_output(f"ARIMA 模型预测 {region} 完成。")
            next_month_data.append(arima_predictions.values)

        except Exception as e:
            append_output(f"ARIMA模型在预测 {region} 时遇到错误：{e}")
            next_month_data.append(np.zeros(30))

    # 构建预测结果数据框
    future_dates = pd.date_range(
        start=data.index.max() + pd.Timedelta(days=1), periods=30
    )
    next_month_df = pd.DataFrame({"日期": future_dates})
    for i, region in enumerate(y_columns):
        next_month_df[region] = next_month_data[i]

    return next_month_df
