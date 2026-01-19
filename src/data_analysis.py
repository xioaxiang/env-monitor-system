import pandas as pd
import numpy as np

class DataAnalyzer:
    """数据分析器：负责对传感器数据进行多维度分析"""

    def __init__(self, data):
        """
        初始化数据分析器
        :param data: 已加载的传感器数据（DataFrame格式）
        """
        self.data = data

    def basic_statistics(self):
        """基础统计分析：均值、中位数、标准差、最值"""
        stats = {}
        # 只分析数值型指标
        for column in ['temperature', 'humidity', 'pm25']:
            stats[column] = {
                '均值': round(self.data[column].mean(), 2),
                '中位数': round(self.data[column].median(), 2),
                '标准差': round(self.data[column].std(), 2),
                '最小值': round(self.data[column].min(), 2),
                '最大值': round(self.data[column].max(), 2)
            }
        # 转为DataFrame，方便查看
        return pd.DataFrame(stats).T

    def location_analysis(self):
        """按监测站点分组分析"""
        return self.data.groupby('location').agg({
            'temperature': ['mean', 'std'],
            'humidity': ['mean', 'std'],
            'pm25': ['mean', 'std', 'max']
        }).round(2)

    def time_trend(self):
        """按日期分析日均指标"""
        daily_avg = self.data.groupby(self.data['date'].dt.date).agg({
            'temperature': 'mean',
            'humidity': 'mean',
            'pm25': 'mean'
        }).reset_index()
        return daily_avg

    def air_quality_assessment(self):
        """空气质量评估（基于PM2.5）"""
        def get_aqi_level(pm25):
            """根据PM2.5值判断空气质量等级"""
            if pm25 <= 35:
                return '优'
            elif pm25 <= 75:
                return '良'
            elif pm25 <= 115:
                return '轻度污染'
            elif pm25 <= 150:
                return '中度污染'
            elif pm25 <= 250:
                return '重度污染'
            else:
                return '严重污染'

        # 添加空气质量列
        self.data['air_quality'] = self.data['pm25'].apply(get_aqi_level)

        # 统计各等级天数
        quality_count = self.data['air_quality'].value_counts()
        # 计算优良天数比例
        good_days = (self.data['pm25'] <= 75).sum()
        good_ratio = f"{good_days/len(self.data)*100:.1f}%"

        return {
            '空气质量分布': quality_count,
            '优良天数比例': good_ratio
        }

    def temperature_extremes(self):
        """温度极值分析"""
        # 高温（>30℃）、低温（<15℃）天数
        hot_days = len(self.data[self.data['temperature'] > 30])
        cold_days = len(self.data[self.data['temperature'] < 15])
        # 最高/最低温日期
        max_temp_date = self.data.loc[self.data['temperature'].idxmax(), 'date']
        min_temp_date = self.data.loc[self.data['temperature'].idxmin(), 'date']

        return {
            '高温天数(>30℃)': hot_days,
            '低温天数(<15℃)': cold_days,
            '最高温日期': max_temp_date.strftime('%Y-%m-%d'),
            '最低温日期': min_temp_date.strftime('%Y-%m-%d')
        }

# 测试代码
if __name__ == '__main__':
    # 导入数据加载器
    from data_loader import DataLoader

    # 加载数据
    loader = DataLoader()
    data = loader.load_data()

    # 创建分析器实例
    analyzer = DataAnalyzer(data)

    print("=== 📈 基础统计分析 ===")
    print(analyzer.basic_statistics())

    print("\n=== 📍 站点分析 ===")
    print(analyzer.location_analysis())

    print("\n=== 🌱 空气质量评估 ===")
    aq_result = analyzer.air_quality_assessment()
    print(f"空气质量分布：\n{aq_result['空气质量分布']}")
    print(f"优良天数比例：{aq_result['优良天数比例']}")

    print("\n=== ❄️ 温度极值分析 ===")
    temp_result = analyzer.temperature_extremes()
    for key, value in temp_result.items():
        print(f"{key}: {value}")