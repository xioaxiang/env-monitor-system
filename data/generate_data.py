import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 设置随机种子（保证每次生成的数据一致）
np.random.seed(42)

# 生成30天的传感器数据
start_date = datetime(2024, 1, 1)
dates = [start_date + timedelta(days=i) for i in range(30)]

# 生成模拟数据
data = {
    'date': dates,
    'temperature': np.random.normal(25, 5, 30),  # 温度：均值25℃，标准差5
    'humidity': np.random.normal(60, 10, 30),    # 湿度：均值60%，标准差10
    'pm25': np.random.normal(50, 20, 30),         # PM2.5：均值50μg/m³，标准差20
    'location': ['站点A']*15 + ['站点B']*15
}

df = pd.DataFrame(data)

# 确保数值在合理范围（湿度0-100，PM2.5≥0）
df['humidity'] = df['humidity'].clip(0, 100)
df['pm25'] = df['pm25'].clip(0, 500)

# 保存数据到data目录
df.to_csv('sensor_data.csv', index=False, encoding='utf-8')
print("传感器数据已生成！")
print("前5行数据：")
print(df.head())